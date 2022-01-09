package cmpecoin;

import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.InvalidKeySpecException;

import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class CmpETransaction {

	public static class Builder {
		private PublicKey fromAddress;
		private PublicKey toAddress;
		private double amount;
		private long timeStamp;
		private CmpETransactionType transactionType;

		public CmpETransaction create(){
			CmpETransaction trx = new CmpETransaction();
			trx.fromAddress = this.fromAddress;
			trx.toAddress = this.toAddress;
			trx.amount = this.amount;
			trx.timeStamp = this.timeStamp;
			trx.transactionType = this.transactionType;
			return trx;
		}

		public Builder fromAddress(PublicKey _fromAddress){
			this.fromAddress = _fromAddress;
			return this;
		}
		public Builder toAddress(PublicKey _toAddress){
			this.toAddress = _toAddress;
			return this;
		}
		public Builder amount(Double _amount){
			this.amount = _amount;
			return this;
		}
		public Builder timestamp(Long _timestamp){
			this.timeStamp = _timestamp;
			return this;
		}
		public Builder transactionType(CmpETransactionType _transactionType){
			this.transactionType = _transactionType;
			return this;
		}
	}

	private String transactionHash;
	private PublicKey fromAddress;
	private PublicKey toAddress;
	private double amount;
	private long timeStamp;
	private byte[] signature;
	private CmpETransactionType transactionType;

	private CmpETransaction() {

	}

	byte[] calculateTransactionHash() throws NoSuchAlgorithmException {
		MessageDigest digest = MessageDigest.getInstance("SHA-256");
		String hashed = fromAddress.toString() + toAddress.toString() +
				Double.toString(amount) + Long.toString(timeStamp);
		byte[] tHash = digest.digest(hashed.getBytes(StandardCharsets.UTF_8));
		return tHash;
	}

	public void signTransaction(PrivateKey secretKey)
			throws NoSuchAlgorithmException, InvalidKeyException, SignatureException {

		// --> DONE! => TODO: If needed, hash the data before sign
		byte[] trxHash = this.calculateTransactionHash();
		this.transactionHash = new String(trxHash, StandardCharsets.UTF_8);

		Signature sign = Signature.getInstance("SHA256withDSA");
		sign.initSign(secretKey);
		sign.update(trxHash);
		byte[] realSig = sign.sign();
		this.signature = realSig;
	}

	public String getTransactionHash() {
		return transactionHash;
	}

	PublicKey getFromAddress() {
		return fromAddress;
	}

	PublicKey getToAddress() {
		return toAddress;
	}

	long getTimestamp() {
		return timeStamp;
	}

	double getAmount() {
		return amount;
	}

	// --> DONE! => TODO: Add transaction type
	public boolean isTransactionValid()
			throws InvalidKeyException, NoSuchAlgorithmException, SignatureException, InvalidKeySpecException {
		/*
		--> DONE! => TODO: Add balance check, discuss with the instructor.
		Balance check should be in the clients,
		if client has less than the desired amount,
		then it should not be allowed.
		*/

		switch (this.transactionType){
			case REGULAR -> {
				return verifySignature();
			}
			case BALANCE -> {
				return this.fromAddress == null && this.getAmount() == 100.0;
			}
			case REWARD -> {
				return this.fromAddress == null && this.getAmount() == 1.0;
			}
		}

		return false;
	}

	boolean verifySignature()
			throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
		Signature signature = Signature.getInstance("SHA256WithDSA");

		// --> DONE! => TODO: Use transactionHash to verify the signature
		KeyFactory factory = KeyFactory.getInstance("RSA");
		byte[] fAddress = fromAddress.toString().getBytes();
		X509EncodedKeySpec encodedKeySpec = new X509EncodedKeySpec(fAddress);
		PublicKey pKey = factory.generatePublic(encodedKeySpec);

		signature.initVerify(pKey);
		signature.update(this.transactionHash.getBytes(StandardCharsets.UTF_8));
		return signature.verify(this.signature);
	}

	public String getSerializedTransaction() {
		if(signature == null){
			return Base64.getEncoder().encodeToString(fromAddress.getEncoded()) + "_" +
					Base64.getEncoder().encodeToString(toAddress.getEncoded()) + "_" +
					amount + "_" +
					timeStamp + "_" +
					"$";
		}
		return Base64.getEncoder().encodeToString(fromAddress.getEncoded()) + "_" +
				Base64.getEncoder().encodeToString(toAddress.getEncoded()) + "_" +
				amount + "_" +
				timeStamp + "_" +
				new String(signature, StandardCharsets.UTF_8);
	}

	public static CmpETransaction getDeserialized(String transactionString)
			throws NoSuchAlgorithmException, InvalidKeySpecException {
		String[] split = transactionString.split("_");
		byte[] fromKeyBytes = Base64.getDecoder().decode(split[0]);
		byte[] toKeyBytes = Base64.getDecoder().decode(split[0]);
		X509EncodedKeySpec fromSpec = new X509EncodedKeySpec(fromKeyBytes);
		X509EncodedKeySpec toSpec = new X509EncodedKeySpec(toKeyBytes);
		KeyFactory factory = KeyFactory.getInstance("DSA");
		PublicKey fromPubKey = factory.generatePublic(fromSpec);
		PublicKey toPubKey = factory.generatePublic(toSpec);
		CmpETransaction trx = new Builder()
				.fromAddress(fromPubKey)
				.toAddress(toPubKey)
				.amount(Double.parseDouble(split[2]))
				.timestamp(Long.parseLong(split[3]))
				.create();
		trx.signature = split[4].getBytes(StandardCharsets.UTF_8);
		return trx;
	}
}

