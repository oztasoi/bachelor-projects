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


// TODO ADD BLOCKCHAIN
public class CmpEValidatorNode {
    public final String LOCALHOST = "127.0.0.1";
    private final String netwDispatcherAddress = LOCALHOST + ":5000";
    public CmpEWallet myWallet;
    private ServerSocket serverSocket;
    private CmpEBlockchain blockChain;
    private String myAddress;
    private int id;

    public CmpEValidatorNode(int _id)
            throws IOException, NoSuchAlgorithmException,
            SignatureException, InvalidKeySpecException, InvalidKeyException {
        // Console input handler node
        new CmpEValidatorNode.ConsoleHandler(this).start();
        this.id = _id;
        this.myAddress = LOCALHOST + ":" + (5300 + _id);
        myWallet = new CmpEWallet();
        blockChain = new CmpEBlockchain(1.0, 2);
        start(5400 + _id);
    }


    public void start(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        serverSocket.setReuseAddress(true);
        System.out.println("listening port " + port + "..");
        while(true){
            new CmpEValidatorNode.ValidatorNodeHandler(serverSocket.accept(), this).start();
        }
    }

    public void joinCmpECoinNetw() throws IOException {
        CmpEMessage msg = new CmpEMessage.Builder()
                .fromSource(myAddress)
                .withType(CmpEMessageType.JOIN_VALIDATOR)
                .toTarget(netwDispatcherAddress)
                .atUNIX(Instant.now().getEpochSecond())
                .addJson(CmpEMessage.jsonify("I AM A GODDAMN VALIDATOR!"))
                .create();
        sendMessage(netwDispatcherAddress, msg);
    }

    public void handleReceivedValidatedBlock(CmpEMessage data) {
        CmpEBlock dummy = new CmpEBlock.Builder().create();
        CmpEBlock valBlock = (CmpEBlock) data.getJsonDeserialized(dummy);
        blockChain.chain.add((valBlock));
    }

    public void handleReceivedTransactions(CmpEMessage data)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        CmpETransaction trx = CmpETransaction.getDeserialized(data.getJsonString());
        System.out.println(trx);
        blockChain.pendingTransactions.add(trx);
    }

    public void handleBeaconAndStartValidationProc()
            throws NoSuchAlgorithmException, SignatureException,
            InvalidKeySpecException, InvalidKeyException, IOException {
        CmpEBlock validatedBlock = blockChain.validatePendingTransactions(myWallet.getPublicKey(),false);
        if (validatedBlock != null){
            CmpEMessage msg = new CmpEMessage.Builder()
                    .fromSource(myAddress)
                    .withType(CmpEMessageType.BLOCK)
                    .toTarget(netwDispatcherAddress)
                    .atUNIX(Instant.now().getEpochSecond())
                    .addJson(CmpEMessage.jsonify(validatedBlock))
                    .create();
            sendMessage(netwDispatcherAddress, msg);
        }
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

    private static class ValidatorNodeHandler extends Thread {
        private CmpEValidatorNode vNode;
        private Socket clientSocket;
        private PrintWriter out;
        private BufferedReader in;

        public ValidatorNodeHandler(Socket socket, CmpEValidatorNode vNode) {
            this.clientSocket = socket;
            this.vNode = vNode;
        }

        public void run() {
            String strMsg = parseInput();
            CmpEMessage msg = CmpEMessage.fromString(strMsg);
            if (msg.getMessageType() == CmpEMessageType.BLOCK_BC){
                vNode.handleReceivedValidatedBlock(msg);
            } else if (msg.getMessageType() == CmpEMessageType.TRANSACTION_BC){
                try {
                    vNode.handleReceivedTransactions(msg);
                } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
                    e.printStackTrace();
                }
            } else if (msg.getMessageType() == CmpEMessageType.BEACON){
                try {
                    vNode.handleBeaconAndStartValidationProc();
                } catch
                (NoSuchAlgorithmException | SignatureException |
                                InvalidKeySpecException | InvalidKeyException | IOException e) {
                    e.printStackTrace();
                }
            } else if (msg.getMessageType() == CmpEMessageType.JOIN_CLIENT) {
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
                        Set<PublicKey> tSet = new HashSet<PublicKey>(vNode.blockChain.clientPublicKeyList);
                        if(!tSet.contains(pubKey)) {
                            vNode.blockChain.clientPublicKeyList.add(pubKey);
                            if(vNode.blockChain.clientPublicKeyList.size() == 3){
                                System.out.println("Let's Create Genesis Block!");
                                vNode.blockChain.createInitialDummyBlock();
                            }
                        }
                    } catch (NoSuchAlgorithmException | InvalidKeySpecException |
                            SignatureException | InvalidKeyException e) {
                        e.printStackTrace();
                    }
                }
                System.out.println("Client Public Keys Added.");
            }
            else {
                System.out.println("We are beautiful!");
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
                    if ("$".equals(inputLine)) {
                        System.out.println(buffer);
                        out.println("Received Transaction");
                        break;
                    }
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

    private static class ConsoleHandler extends Thread{
        private CmpEValidatorNode vNode;
        private ConsoleHandler(CmpEValidatorNode _vNode) {
            this.vNode = _vNode;
        }

        @Override
        public void run(){
            Scanner scanner = new Scanner(System.in);
            String input = scanner.nextLine();
            while(!input.equals("exit")){
                System.out.println("input received: " + input);
                if (input.equals("join")){
                    try {
                        vNode.joinCmpECoinNetw();
                        System.out.println("JOIN!");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                // todo process inputs
                input = scanner.nextLine();
            }
            System.out.println("shutting down..");
            System.exit(0);
        }
    }
}
