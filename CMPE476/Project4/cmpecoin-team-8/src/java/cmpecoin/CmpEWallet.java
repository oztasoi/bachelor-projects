package cmpecoin;

import java.security.*;

public class CmpEWallet {
    private PublicKey publicKey;
    private PrivateKey privateKey;
    private double currentBalance;

    public CmpEWallet() throws NoSuchAlgorithmException {
        this.initWallet();
        System.out.println("wallet created, public key: " + this.publicKey);
    }

    /*
    - Inspired from https://www.tutorialspoint.com/java_cryptography/java_cryptography_keypairgenerator.htm
     */
    public void initWallet() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("DSA");
        keyPairGen.initialize(2048);
        KeyPair pair = keyPairGen.generateKeyPair();
        this.privateKey = pair.getPrivate();
        this.publicKey = pair.getPublic();
    }

    public PublicKey getPublicKey(){
        return this.publicKey;
    }

    public PrivateKey getPrivateKey(){
        return this.privateKey;
    }

    public double getCurrentBalance(){
        return this.currentBalance;
    }

    public void setCurrentBalance(double newBalance){
        this.currentBalance = newBalance;
    }
}
