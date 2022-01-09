package test;

import java.security.InvalidKeyException;
import java.security.SignatureException;
import java.time.Instant;
import java.util.Date;

import cmpecoin.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import static org.junit.Assert.assertEquals;

public class CmpENetwDispatcherTest {
    int port = 5000;
    CmpESimpleNode client;

    @Before
    public void setup() throws IOException, NoSuchAlgorithmException {
        client = new CmpESimpleNode(1);
        client.start(port);
    }
    @After
    public void tearDown() throws IOException {
        //client.stopConnection();
    }

    @Test
    public void simpleNodeTransaction() throws IOException, NoSuchAlgorithmException, SignatureException, InvalidKeyException {
        client.myWallet = new CmpEWallet();
        CmpEWallet targetWallet = new CmpEWallet();
        CmpETransaction transaction = new CmpETransaction.Builder()
                .fromAddress(client.myWallet.getPublicKey())
                .toAddress(targetWallet.getPublicKey())
                .amount(50.0)
                .timestamp(Instant.now().getEpochSecond())
                .transactionType(CmpETransactionType.REGULAR)
                .create();
        transaction.signTransaction(client.myWallet.getPrivateKey());

        //String msg1 = client.requestTransaction(transaction);
        //assertEquals("Received Transaction", msg1);
    }
}
