package test;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.runners.MockitoJUnitRunner;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.time.Instant;

import cmpecoin.CmpEBlock;


@RunWith(MockitoJUnitRunner.class)
class CmpEBlockTest {

    @BeforeEach
    public void setup(){
        MockitoAnnotations.initMocks(this);
    }

    @Test
    void invalidateBlockWhenInvalid() throws
            NoSuchAlgorithmException,
            SignatureException,
            InvalidKeySpecException,
            InvalidKeyException {

        CmpEBlock block = new CmpEBlock.Builder()
                .addPrevBlockHash("prevBlockHash")
                .insertTransactions(null)
                .createdTimestamp(Instant.now().getEpochSecond())
                .create();

        CmpEBlock block1 = Mockito.spy(block);
        Mockito.doReturn(null).when(block1).calculateCurrBlockHash();
        boolean isValid = block1.validateBlock(13);

        Assertions.assertFalse(isValid);
    }

    @Test
    void validateBlockWhenValid() throws
            NoSuchAlgorithmException,
            SignatureException,
            InvalidKeySpecException,
            InvalidKeyException {

        CmpEBlock block = new CmpEBlock.Builder()
                .addPrevBlockHash("prevBlockHash")
                .insertTransactions(null)
                .createdTimestamp(Instant.now().getEpochSecond())
                .create();

        CmpEBlock block1 = Mockito.spy(block);
        Mockito.doReturn("a").when(block1).calculateCurrBlockHash();
        boolean isValid = block1.validateBlock(13);

        Assertions.assertTrue(isValid);
    }
}