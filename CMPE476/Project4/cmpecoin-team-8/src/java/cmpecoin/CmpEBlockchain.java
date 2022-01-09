package cmpecoin;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class CmpEBlockchain {

    int difficulty;
    double validationReward;
    CmpEBlock initialBlock;
    LinkedList<CmpEBlock> chain;
    ArrayList<PublicKey> clientPublicKeyList;
    ArrayList<CmpETransaction> pendingTransactions;

    public CmpEBlockchain(double _validationReward, int _difficulty){
        this.validationReward = _validationReward;
        this.difficulty = _difficulty;
        this.chain = new LinkedList<CmpEBlock>();
        this.pendingTransactions = new ArrayList<CmpETransaction>();
        this.clientPublicKeyList = new ArrayList<PublicKey>();
    }

    void createInitialDummyBlock()
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        // --> DONE DIFFERENTLY! => TODO: If necessary, make this part hardcoded, manually written transactions
        for(PublicKey clientPublicKey: this.clientPublicKeyList){
            pendingTransactions.add(new CmpETransaction.Builder()
                .fromAddress(null)
                .toAddress(clientPublicKey)
                .amount(100.0)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.BALANCE)
                .create()
            );
        }
        // --> DONE! => TODO: Add a new genesis block transaction check mechanism
        initialBlock = validatePendingTransactions(null, true);
        System.out.println("Genesis Block: " + initialBlock.toString());
    }

    public void addClientToTheChain(PublicKey clientPublicKey){
        this.clientPublicKeyList.add(clientPublicKey);
    }

    public boolean isChainValid()
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        // --> DONE! => TODO: Add consecutive block hash consistency check
        CmpEBlock[] chainArr = (CmpEBlock[])chain.toArray();
        for(int i=1; i<chainArr.length; i++){
            if(!chainArr[i].validateBlock(difficulty) ||
                    !chainArr[i - 1].getCurrBlockHash().equals(chainArr[i].getPrevBlockHash())) return false;
        }
        return true;
    }

    public void addTransactionToPendingList(CmpETransaction _transaction)
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {
        // TODO: Add another check, think deeper
        if(!_transaction.isTransactionValid() ||
                getBalanceOf(_transaction.getFromAddress()) < _transaction.getAmount()){
            return;
        }
        this.pendingTransactions.add(_transaction);
    }

    public CmpEBlock validatePendingTransactions(PublicKey rewardAddress, boolean isGenesisBlock)
            throws NoSuchAlgorithmException, SignatureException, InvalidKeySpecException, InvalidKeyException {

        if(rewardAddress != null){
            CmpETransaction rewardTrx = new CmpETransaction.Builder()
                    .fromAddress(null)
                    .toAddress(rewardAddress)
                    .amount(validationReward)
                    .timestamp(Instant.now().getEpochSecond())
                    .transactionType(CmpETransactionType.REWARD)
                    .create();
            pendingTransactions.add(rewardTrx);
        }

        CmpEBlock newBlock;
        ArrayList<CmpETransaction> currentPendingTrx;
        synchronized (this){
            currentPendingTrx = pendingTransactions;
            pendingTransactions.clear();
        }
        if(isGenesisBlock){
            newBlock = new CmpEBlock.Builder()
                    .addPrevBlockHash("")
                    .insertTransactions(currentPendingTrx)
                    .createdTimestamp(Instant.now().getEpochSecond())
                    .create();
            chain.add(newBlock);
        } else {
            newBlock = new CmpEBlock.Builder()
                    .addPrevBlockHash(chain.getLast().getCurrBlockHash())
                    .insertTransactions(currentPendingTrx)
                    .createdTimestamp(Instant.now().getEpochSecond())
                    .create();
        }

        if(!isGenesisBlock){
            boolean blockValidation = newBlock.validateBlock(this.difficulty);
            if(!blockValidation){
                System.out.println("Invalid transactions detected in current block.");
                return null;
            }
        }
        // TODO: Add winner condition for the validator network
        return newBlock;
    }

    public float getBalanceOf(PublicKey pubKey){
        float income = 0f;
        float outcome = 0f;
        List<CmpETransaction> trxList = getAllTransactionsFor(pubKey);
        for(CmpETransaction trx: trxList){
            if(trx.getFromAddress().equals(pubKey)){
                outcome += trx.getAmount();
            }
            else if(trx.getToAddress().equals(pubKey)){
                income += trx.getAmount();
            }
        }
        return income - outcome;
    }

    public List<CmpETransaction> getAllTransactionsFor(PublicKey pubKey){
        List<CmpETransaction> allTrxList = new ArrayList<CmpETransaction>();
        CmpEBlock[] allBlockArr = (CmpEBlock[])this.chain.toArray();
        for(CmpEBlock block: allBlockArr){
            List<CmpETransaction> trxArrayList = new ArrayList<CmpETransaction>(block.getTransactions());
            for(CmpETransaction trx: trxArrayList){
                if(trx.getFromAddress().equals(pubKey) || trx.getToAddress().equals(pubKey)){
                    allTrxList.add(trx);
                }
            }
        }
        return allTrxList;
    }
}