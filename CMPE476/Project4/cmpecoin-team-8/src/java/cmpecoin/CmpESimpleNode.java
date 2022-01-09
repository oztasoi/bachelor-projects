package cmpecoin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.TimeUnit;

// TODO ADD BLOCKCHAIN
public class CmpESimpleNode {
    private int id;
    public final String LOCALHOST = "127.0.0.1";
    private final String netwDispatcherAddress = LOCALHOST + ":5000";
    private String myAddress;
    public CmpEWallet myWallet;
    private ArrayList<PublicKey> clientList;
    private ArrayBlockingQueue<CmpEBlock> listenQValidatedBlocksFromNetwDispatcher;
    private double meanTransactionAmount;
    private final double meanTransactionInnerDuration;
    private CmpEBlockchain blockChain;
    private ServerSocket serverSocket;
    private int transactionCount;
    private int tAmountTotal;

    public CmpESimpleNode(int _id) throws IOException, NoSuchAlgorithmException {
        // Console input handler node
        this.id = _id;
        this.myAddress = LOCALHOST + ":" + (5100 + _id);
        new CmpESimpleNode.ConsoleHandler(this).start();
        meanTransactionInnerDuration = 2;
        meanTransactionAmount = 0;
        transactionCount = 0;
        tAmountTotal = 0;
        myWallet = new CmpEWallet();
        clientList = new ArrayList<>();
        start(5200 + _id);
    }

    public void start(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        serverSocket.setReuseAddress(true);
        System.out.println("listening port " + port + "..");
        SimpleNodeHandler handler;
        while (true) {
            handler = new SimpleNodeHandler(serverSocket.accept(), this);
            handler.start();
        }
    }

    public int getRandNode() {
        int size = clientList.size();
        ArrayList<Integer> indexes = new ArrayList<>();
        for(int i =0; i<size; i++) {
            indexes.add(i);
        }
        Collections.shuffle(indexes);
        int to = indexes.get(0);
        while(clientList.get(to) == myWallet.getPublicKey()) {
            Collections.shuffle(indexes);
            to = indexes.get(0);
        }
        return to;
    }

    // TODO AMOUNT VALUE
    public void doRandomTransactions() throws
            InterruptedException, NoSuchAlgorithmException, SignatureException, IOException, InvalidKeyException {
        int node = getRandNode();
        int amount = 20;
        TimeUnit.SECONDS.sleep((long) getRandExp(meanTransactionInnerDuration));

        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(myWallet.getPublicKey())
                .toAddress(blockChain.clientPublicKeyList.get(node))
                .amount(20.0)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .create();
        transaction.signTransaction(myWallet.getPrivateKey());

        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(myAddress)
                .withType(CmpEMessageType.TRANSACTION)
                .toTarget(netwDispatcherAddress)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(transaction.getSerializedTransaction())
                .create();
        sendMessage(netwDispatcherAddress, msg);

        tAmountTotal += amount;
        transactionCount++;
        meanTransactionAmount = tAmountTotal / transactionCount;
    }

    public void doTransaction(int index, double amount)
            throws IOException, NoSuchAlgorithmException, SignatureException, InvalidKeyException {
        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(myWallet.getPublicKey())
                .toAddress(clientList.get(index))
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .amount(amount)
                .create();
        transaction.signTransaction(myWallet.getPrivateKey());

        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(myAddress)
                .toTarget(netwDispatcherAddress)
                .withType(CmpEMessageType.TRANSACTION)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(transaction.getSerializedTransaction())
                .create();
        sendMessage(netwDispatcherAddress, msg);
    }

    private void sendMessage(String address, CmpEMessage msg) throws IOException {
        String[] arr = address.split(":");
        Socket clientSocket = new Socket(arr[0], Integer.parseInt(arr[1]));
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        out.write(msg.toString());
        out.flush();
        out.close();
        clientSocket.close();
    }

    public double getRandExp(double mean) {
        Random rand = new Random();
        return Math.log(1-rand.nextDouble())/(1/-mean);
    }

    public void doRandomInvalidTransaction() throws InterruptedException, IOException {
        int node = getRandNode();
        TimeUnit.SECONDS.sleep((long) getRandExp(meanTransactionInnerDuration));
        double curAmount = myWallet.getCurrentBalance();
        Random rand = new Random();
        int invalidAmount = (int) (rand.nextInt() + curAmount);

        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(myWallet.getPublicKey())
                .toAddress(blockChain.clientPublicKeyList.get(node))
                .amount((double)invalidAmount)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .create();

        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(myAddress)
                .withType(CmpEMessageType.TRANSACTION)
                .toTarget(netwDispatcherAddress)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(transaction.getSerializedTransaction())
                .create();
        sendMessage(netwDispatcherAddress,msg);
    }

    public void joinCmpECoinNetw() throws IOException {
            CmpEMessage msg = new CmpEMessage.Builder()
                    .fromSource(myAddress)
                    .withType(CmpEMessageType.JOIN_CLIENT)
                    .toTarget(netwDispatcherAddress)
                    .atUNIX(Instant.now().getEpochSecond())
                    .addJson(Base64.getEncoder().encodeToString(myWallet.getPublicKey().getEncoded()))
                    .create();
            sendMessage(netwDispatcherAddress,msg);
    }

    public void handleReceivedValidatedBlock(CmpEMessage data) {
        CmpEBlock dummy = new CmpEBlock.Builder().create();
        blockChain.chain.add((CmpEBlock) data.getJsonDeserialized(dummy));
    }

    private static class SimpleNodeHandler extends Thread {
        private CmpESimpleNode sNode;
        private Socket clientSocket;
        private PrintWriter out;
        private BufferedReader in;

        public SimpleNodeHandler(Socket socket, CmpESimpleNode sNode) {
            this.clientSocket = socket;
            this.sNode = sNode;
        }

        public void run() {
            String strMsg = parseInput();
            CmpEMessage msg = CmpEMessage.fromString(strMsg);
            if (msg.getMessageType() == CmpEMessageType.BLOCK_BC){
                sNode.handleReceivedValidatedBlock(msg);
            } else if (msg.getMessageType() == CmpEMessageType.JOIN_CLIENT){
                String[] a = new String[3];
                String[] encodedPubKeyArr = (String[]) msg.getJsonDeserialized(a);
                for(String encodedPubKeyStr: encodedPubKeyArr){
                    byte[] pubKeyByteArr = Base64.getDecoder().decode(encodedPubKeyStr);
                    try {
                        PublicKey pubKey = KeyFactory
                                .getInstance("DSA")
                                .generatePublic(
                                        new X509EncodedKeySpec(pubKeyByteArr)
                                );
                        System.out.println("Public Key Generated.");
                        if(!sNode.myWallet.getPublicKey().equals(pubKey)){
                            // TODO: remove same pubKeys
                            Set<PublicKey> tSet = new HashSet<PublicKey>(sNode.clientList);
                            if(!tSet.contains(pubKey)) sNode.clientList.add(pubKey);
                        } else {
                            System.out.println("My key received.");
                        }
                    } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
                        e.printStackTrace();
                    }
                }
                System.out.println("Client Public Keys Added.");
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

    private static class ClientActionTaker {

        private String[] tokens;
        private CmpESimpleNode sNode;

        public ClientActionTaker(CmpESimpleNode _sNode){
            this.sNode = _sNode;
        }

        public void setTokens(String[] _tokens){
            this.tokens = _tokens;
        }

        public void decideAct()
                throws IOException, NoSuchAlgorithmException, SignatureException, InvalidKeyException {
            if(tokens[0].equals("transaction")){
                System.out.println("Transaction operation is started.");
                sNode.doTransaction(Integer.parseInt(tokens[1]), Double.parseDouble(tokens[2]));
            } else if (tokens[0].equals("join")){
                System.out.println("Joining the network, please wait.");
                sNode.joinCmpECoinNetw();
                System.out.println("Joining the network operation successfully done.");
            } else if (tokens[0].equals("randomvalid")){
                System.out.println("Attempting random valid transaction implosion on the system.");
                try {
                    sNode.doRandomTransactions();
                } catch (InterruptedException |
                        NoSuchAlgorithmException |
                        SignatureException |
                        IOException |
                        InvalidKeyException e) {
                    e.printStackTrace();
                }
            } else if (tokens[0].equals("randominvalid")){
                System.out.println("Attempting random invalid transaction implosion on the system.");
                try {
                    sNode.doRandomInvalidTransaction();
                } catch (InterruptedException | IOException e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("Nothing!");
            }
        }
    }

    private static class ConsoleHandler extends Thread{

        private ClientActionTaker manager;

        public ConsoleHandler(CmpESimpleNode _sNode){
            this.manager = new ClientActionTaker(_sNode);
        }

        @Override
        public void run(){
            Scanner scanner = new Scanner(System.in);
            String input = scanner.nextLine();
            while(!input.equals("exit")){
                String[] tokens = input.split("\\s");

                manager.setTokens(tokens);
                try {
                    manager.decideAct();
                } catch (IOException | NoSuchAlgorithmException | SignatureException | InvalidKeyException e) {
                    e.printStackTrace();
                }
                input = scanner.nextLine();
            }
            System.out.println("shutting down..");
            try {
                manager.sNode.serverSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            System.exit(0);
        }
    }
}

