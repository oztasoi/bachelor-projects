package cmpecoin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;

public class CmpENetwDispatcher {

    public final String LOCALHOST = "127.0.0.1";
    private ServerSocket serverSocket;
    private ArrayBlockingQueue<CmpETransaction> transxRcvQ;
    private ArrayBlockingQueue<cmpecoin.CmpEBlock> validatedBlockRcvQ;
    private HashMap<String, Enum> joinedNodeAddresses;
    private HashSet<PublicKey> clientWallets;
    private TransactionServer trxServer;
    private ValidatorServer vlxServer;
    private BeaconServer beaconServer;
    private boolean isValBlockReceived;

    public CmpENetwDispatcher() throws IOException {
        transxRcvQ = new ArrayBlockingQueue<CmpETransaction>(30);
        validatedBlockRcvQ = new ArrayBlockingQueue<cmpecoin.CmpEBlock>(30);
        joinedNodeAddresses = new HashMap<String, Enum>();
        clientWallets = new HashSet<PublicKey>();
        // Transaction communication handler node
        int TransactionServerPort = 5000;
        trxServer = new TransactionServer(this, TransactionServerPort);
        trxServer.start();
        // Validator communication handler node
//        int ValidatorServerPort = 5001;
//        vlxServer = new ValidatorServer(this, ValidatorServerPort);
//        vlxServer.start();
        // Console input handler node
//        int BeaconServerPort = 5002;
//        beaconServer = new BeaconServer(this, BeaconServerPort);
//        beaconServer.start();
        new CmpENetwDispatcher.ConsoleHandler(this).start();

        System.out.println("Succesfully started the dispatcher server");
    }

    public void start(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        serverSocket.setReuseAddress(true);
        System.out.println("listening port " + port + "..");
        while(true){
            new DispatcherHandler(serverSocket.accept(), this).start();
        }
    }

    public void stop() throws IOException {
        serverSocket.close();
    }

    private ArrayList<String> getAddressList(Enum type){
         ArrayList<String> list = new ArrayList<String>();
         for (String address : joinedNodeAddresses.keySet()){
             if(joinedNodeAddresses.get(address) == type){
                 list.add(address);
             }
         }
         return list;
    }

    private String[] getPreppedPubKeys(){
        Iterator<PublicKey> it = clientWallets.iterator();
        int pubKeyListLength = clientWallets.toArray().length;
        String[] encodedPubKeyArr = new String[pubKeyListLength];
        int index = 0;
        while(it.hasNext()){
            encodedPubKeyArr[index] = Base64.getEncoder().encodeToString(it.next().getEncoded());
            index++;
        }
        return encodedPubKeyArr;
    }

    public void broadcastReceivedTransx() throws IOException {
        for (String address : getAddressList(CmpENodeType.VALIDATOR)){
                CmpEMessage msg = new CmpEMessage.Builder()
                    .fromSource(LOCALHOST)
                    .withType(CmpEMessageType.TRANSACTION_BC)
                    .toTarget(address)
                    .atUNIX(Instant.now().getEpochSecond())
                    .addJson(transxRcvQ.peek().getSerializedTransaction())
                    .create();
            sendMessage(address,msg);
        }
    }

    public void broadcastLastValidatedBlock() throws IOException {
        for (String address : joinedNodeAddresses.keySet()){
            CmpEMessage msg = new CmpEMessage.Builder()
                    .fromSource(LOCALHOST)
                    .withType(CmpEMessageType.BLOCK_BC)
                    .toTarget(address)
                    .atUNIX(Instant.now().getEpochSecond())
                    .addJson(CmpEMessage.jsonify((CmpEBlock)validatedBlockRcvQ.peek()))
                    .create();
            sendMessage(address,msg);
        }
    }

    private void sendMessage(String address, CmpEMessage msg) throws IOException {
        String[] arr = address.split(":");
        Socket clientSocket = new Socket(arr[0], Integer.parseInt(arr[1]));
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        out.write(msg.toString());
        out.close();
        clientSocket.close();
    }

    public void broadcastValidationBeacon() throws IOException {
        for (String address : getAddressList(CmpENodeType.VALIDATOR)){
            CmpEMessage msg = new CmpEMessage.Builder()
                    .fromSource(LOCALHOST)
                    .withType(CmpEMessageType.BEACON)
                    .toTarget(address)
                    .atUNIX(Instant.now().getEpochSecond())
                    .addJson(CmpEMessage.jsonify(null))
                    .create();
            sendMessage(address,msg);
        }
    }

    public void sendCurrentBlockChainTo(String address) throws IOException {
        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(LOCALHOST)
                .withType(CmpEMessageType.BLOCKCHAIN)
                .toTarget(address)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(CmpEMessage.jsonify((ArrayBlockingQueue)validatedBlockRcvQ))
                .create();
        sendMessage(address, msg);
    }

    public void sendSimpleNodeAddresses(String address) throws IOException {
        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(LOCALHOST)
                .withType(CmpEMessageType.BLOCKCHAIN)
                .toTarget(address)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(CmpEMessage.jsonify(getAddressList(CmpENodeType.CLIENT)))
                .create();
        sendMessage(address, msg);
    }

    private static class DispatcherHandler extends Thread {
        private CmpENetwDispatcher dispatcher;
        private Socket clientSocket;
        private PrintWriter out;
        private BufferedReader in;

        public DispatcherHandler(Socket socket, CmpENetwDispatcher dispatcher) {
            this.clientSocket = socket;
            this.dispatcher = dispatcher;
        }

        private String calculateListenerBySender(String fromSender){
            String[] arr = fromSender.split(":");
            return arr[0] + ":" + (Integer.parseInt(arr[1]) + 100);
        }

        public void run() {
           String strMsg = parseInput();
           CmpEMessage msg = CmpEMessage.fromString(strMsg);
           System.out.println(strMsg);
           if (msg.getMessageType() == CmpEMessageType.BLOCK){
               try {
                   if(!this.dispatcher.isValBlockReceived){
                       CmpEBlock dummy = new CmpEBlock.Builder().create();
                       synchronized (this){
                           if(!this.dispatcher.isValBlockReceived){
                               dispatcher.isValBlockReceived = true;
                               dispatcher.validatedBlockRcvQ.add((CmpEBlock) msg.getJsonDeserialized(dummy));
                               dispatcher.broadcastLastValidatedBlock();
                           }
                       }
                   }
               } catch (IOException e) {
                   e.printStackTrace();
               }
           } else if (msg.getMessageType() == CmpEMessageType.TRANSACTION){
               try {
                   synchronized (this){
                       dispatcher.transxRcvQ.add(
                               CmpETransaction.getDeserialized(msg.getJsonString())
                       );
                   }
                   dispatcher.broadcastReceivedTransx();
               } catch (IOException | NoSuchAlgorithmException | InvalidKeySpecException e) {
                   e.printStackTrace();
               }
           } else if (msg.getMessageType() == CmpEMessageType.JOIN_CLIENT){
               try {
                   byte[] pubKeyBytes = Base64.getDecoder().decode(msg.getJsonString());
                   X509EncodedKeySpec spec = new X509EncodedKeySpec(pubKeyBytes);
                   KeyFactory factory = KeyFactory.getInstance("DSA");
                   PublicKey key = factory.generatePublic(spec);
                   dispatcher.clientWallets.add(key);

                   dispatcher.joinedNodeAddresses.put(
                           calculateListenerBySender(msg.getSourceAddress()),
                           CmpENodeType.CLIENT);

                   // This is for Public Keys
                   CmpEMessage response = new CmpEMessage.Builder()
                           .fromSource(dispatcher.LOCALHOST + ":5100")
                           .toTarget(calculateListenerBySender(msg.getSourceAddress()))
                           .atUNIX(Instant.now().getEpochSecond())
                           .withType(CmpEMessageType.JOIN_CLIENT)
                           .addJson(CmpEMessage.jsonify(dispatcher.getPreppedPubKeys()))
                           .create();

                   for(String client: dispatcher.getAddressList(CmpENodeType.CLIENT)){
                       dispatcher.sendMessage(client, response);
                   }
                   for(String client: dispatcher.getAddressList(CmpENodeType.VALIDATOR)){
                       dispatcher.sendMessage(client, response);
                   }

               } catch (NoSuchAlgorithmException | IOException | InvalidKeySpecException e) {
                   e.printStackTrace();
               }
           } else if (msg.getMessageType() == CmpEMessageType.JOIN_VALIDATOR) {
               dispatcher.joinedNodeAddresses.put(
                       calculateListenerBySender(msg.getSourceAddress()),
                       CmpENodeType.VALIDATOR);
           }
        }
        public String parseInput(){
            try {
                out = new PrintWriter(clientSocket.getOutputStream(), true);
                in = new BufferedReader(
                        new InputStreamReader(clientSocket.getInputStream()));

                String inputLine;
                StringBuilder buffer = new StringBuilder();
                while ((inputLine = in.readLine()) != null) {
                    System.out.println(buffer);
                    out.println("Received Transaction");
                    buffer.append(inputLine);
                }

                in.close();
                out.close();
                clientSocket.close();
                return buffer.toString();
            }
            catch (IOException e) {
                e.printStackTrace();
                return e.getMessage();
            }
        }
    }
    private static class BeaconServer extends Thread{
        CmpENetwDispatcher node;
        int port;
        public BeaconServer(CmpENetwDispatcher node, int port){
            this.node = node;
            this.port = port;
        }
        @Override
        public void run(){
            try {
                node.start(this.port);
                while (true){
                    Thread.sleep(15000);
                    node.isValBlockReceived = false;
                    node.broadcastValidationBeacon();
                }

            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private static class TransactionServer extends Thread{
        CmpENetwDispatcher node;
        int port;
        public TransactionServer(CmpENetwDispatcher node, int port){
            this.node = node;
            this.port = port;
        }
        @Override
        public void run(){
            try {
                node.start(this.port);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    private static class ValidatorServer extends Thread{
        CmpENetwDispatcher node;
        int port;
        public ValidatorServer(CmpENetwDispatcher node, int port){
            this.node = node;
            this.port = port;
        }
        @Override
        public void run(){
            try {
                node.start(this.port);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    private static class ConsoleHandler extends Thread{
        CmpENetwDispatcher dNode;

        private ConsoleHandler(CmpENetwDispatcher _dNode){
            this.dNode = _dNode;
        }
        @Override
        public void run(){
            Scanner scanner = new Scanner(System.in);
            String input = scanner.nextLine();
            while(!input.equals("exit")){
                System.out.println("input received: " + input);
                if (input.equals("beacon")){
                    try {
                        System.out.println("BEACON!");
                        dNode.broadcastValidationBeacon();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                // todo process inputs
                input = scanner.nextLine();
            }
            System.out.println("shutting down..");
            try {
                dNode.serverSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            System.exit(0);
        }
    }
}
