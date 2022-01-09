package test;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.BitSet;

class BitSetTest {
    public static void main(String[] args){
        /*
        TODO: Add valid and invalid bit controller
         test cases to prove our way of proof of work.
         */
        ByteBuffer bb = ByteBuffer.allocate(Long.BYTES);
        bb.putLong(127);

        BitSet b = BitSet.valueOf(bb.array());
        int setBitCount = 0;
        for(int i=0; i<b.length(); i++){
            if(b.get(i)){
                System.out.println("SET");
                setBitCount++;
            } else {
                System.out.println("NOT SET");
            }
        }
        System.out.println(setBitCount);
        System.out.println(b.length());
    }
}
