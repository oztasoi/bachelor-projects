package cmpecoin;

import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.time.Instant;

public class Main {

    public static void main(String[] args)
            throws IOException,
            NoSuchAlgorithmException,
            SignatureException,
            InvalidKeySpecException,
            InvalidKeyException {
        String clientType = args[0];
        switch (clientType){
            case "d":
                new CmpENetwDispatcher();
                break;
            case "v":
                new CmpEValidatorNode(Integer.parseInt(args[1]));
                break;
            case "s":
                new CmpESimpleNode(Integer.parseInt(args[1]));
                break;
        }
    }
}
