package test;

import cmpecoin.CmpEWallet;
import cmpecoin.CmpETransaction;
import cmpecoin.CmpETransactionType;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.runners.MockitoJUnitRunner;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.time.Instant;

@RunWith(MockitoJUnitRunner.class)
class CmpETransactionTest {

    @BeforeEach
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @org.junit.jupiter.api.Test
    void validateTransactionWhenValidBalance()
            throws InvalidKeyException,
            NoSuchAlgorithmException,
            SignatureException,
            InvalidKeySpecException {

        CmpEWallet wallet1 = new CmpEWallet();
        CmpEWallet wt1 = Mockito.spy(wallet1);
        CmpEWallet wallet2 = new CmpEWallet();
        CmpEWallet wt2 = Mockito.spy(wallet1);
        wt1.setCurrentBalance(150);
        wt2.setCurrentBalance(0);
        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(wt1.getPublicKey())
                .toAddress(wt2.getPublicKey())
                .amount(100.0)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .create();
        CmpETransaction tr1 = Mockito.spy(transaction);
        Mockito.doNothing().when(tr1).signTransaction(wt1.getPrivateKey());

        Assertions.assertTrue(transaction.isTransactionValid());
    }

    @org.junit.jupiter.api.Test
    void invalidateTransactionWhenInvalidBalance()
            throws InvalidKeyException,
            NoSuchAlgorithmException,
            SignatureException,
            InvalidKeySpecException {

        CmpEWallet wallet1 = new CmpEWallet();
        CmpEWallet wt1 = Mockito.spy(wallet1);
        CmpEWallet wallet2 = new CmpEWallet();
        CmpEWallet wt2 = Mockito.spy(wallet1);
        wt1.setCurrentBalance(50);
        wt2.setCurrentBalance(0);
        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(wt1.getPublicKey())
                .toAddress(wt2.getPublicKey())
                .amount(100.0)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .create();
        CmpETransaction tr1 = Mockito.spy(transaction);
        Mockito.doNothing().when(tr1).signTransaction(wt1.getPrivateKey());

        Assertions.assertFalse(transaction.isTransactionValid());
    }
}