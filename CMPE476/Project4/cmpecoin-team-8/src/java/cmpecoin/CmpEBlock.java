package cmpecoin;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.time.Instant;
import java.util.BitSet;
import java.util.List;

public class CmpEBlock {

    public static class Builder {
        private String prevBlockHash;
        private String currBlockHash;
        private Long createdTimestamp;
        private Long proofOfWork;
        private List<CmpETransaction> transactions;

        public CmpEBlock create(){
            CmpEBlock block = new CmpEBlock();
            block.prevBlockHash = this.prevBlockHash;
            block.transactions = this.transactions;
            block.createdTimestamp = this.createdTimestamp;
            return block;
        }

        public Builder addPrevBlockHash(String _prevBlockHash){
            this.prevBlockHash = _prevBlockHash;
            return this;
        }
        public Builder insertTransactions(List<CmpETransaction> _transactions){
            this.transactions = _transactions;
            return this;
        }
        public Builder createdTimestamp(Long _createdTimestamp){
            this.createdTimestamp = _createdTimestamp;
            return this;
        }
    }

    private String prevBlockHash;
    private String currBlockHash;
    private Long createdTimestamp;
    private Long validatedTimestamp;
    private Long proofOfWork;
    private List<CmpETransaction> transactions;

    private CmpEBlock(){
        this.proofOfWork = 0L;
    }

    public String calculateCurrBlockHash()
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        if(!hasValidTransactions()){
            return null;
        }

        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        String hashed = prevBlockHash;
        // --> DONE! => TODO: Transaction string
        for(CmpETransaction trx: transactions){
            hashed += trx.getSerializedTransaction();
        }

        hashed += this.proofOfWork;
        byte[] bHash = digest.digest(hashed.getBytes(StandardCharsets.UTF_8));

        return new String(bHash, StandardCharsets.UTF_8);
    }

    public boolean validateBlock(long difficulty)
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        while(true){
            String bHash = calculateCurrBlockHash();
            if(bHash == null) return false;

            byte[] bHashBinary = bHash.getBytes(StandardCharsets.UTF_8);
            ByteBuffer bb = ByteBuffer.wrap(bHashBinary);
            bb.put(bHashBinary);

            BitSet b = BitSet.valueOf(bb.array());
            if(checkDifficulty(b, difficulty)){
                this.currBlockHash = bHash;
                this.validatedTimestamp = Instant.now().getEpochSecond();
                break;
            }
            this.proofOfWork = SecureRandom.getInstanceStrong().nextLong();
        }
        return true;
    }

    // TODO: Add unit test for checking
    private boolean checkDifficulty(BitSet b, long difficulty){
        for(int i=0;i<difficulty;i++){
            if(b.get(i)) return false;
        }
        return true;
    }

    private boolean hasValidTransactions()
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        for(CmpETransaction trx: transactions){
            if(!trx.isTransactionValid()) transactions.remove(trx);
        }
        return true;
    }

    public List<CmpETransaction> getTransactions(){
        return transactions;
    }

    public String getPrevBlockHash(){
        return prevBlockHash;
    }

    public String getCurrBlockHash(){
        return currBlockHash;
    }

    public Long getCreatedTimestamp(){
        return createdTimestamp;
    }

    public Long getValidatedTimestamp(){
        return validatedTimestamp;
    }
}
