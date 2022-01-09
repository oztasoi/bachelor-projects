package project;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.URL;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

import project.MerkleTree.MNode;

public final class Utility {

	public static String padWithZeros(int num) {
		if (num < 10) {
			return num + "";
		} else {
			return padWithZeros(num / 10) + (num % 10);
		}
	}

	public static String nameGenerator(String path) {
		return path.substring(path.lastIndexOf('/') + 1, path.lastIndexOf('.'));

	}

	public static void metaGenerator(String path) throws IOException {
		URL u1 = new URL(path);
		Scanner a = new Scanner(new InputStreamReader(u1.openStream()));
		File q = new File("secondaryPart/" + Utility.nameGenerator(path)+".txt");
		q.createNewFile();
		PrintStream ps = new PrintStream(q);
		while (a.hasNext()) {
			String tt = a.next();
			ps.println(tt);
		}
		a.close();
		ps.close();
	}
	
	public static void jpegMerge(File dir,File output) throws IOException {
		
		FileOutputStream fos = new FileOutputStream(output);
		
		for (File f : dir.listFiles()) {
			FileInputStream fis = new FileInputStream(f);
			byte[] fileBytes = fis.readAllBytes();
			fos.write(fileBytes);
			fos.flush();
			fis.close();
		}
		fos.close();
		
	}
	
	public static int bfsTraversal(String hash, MNode root) {
		Queue<MNode> q = new LinkedList<MNode>();
		q.add(root);
		while(!q.isEmpty()) {
			MNode current = q.poll();
			if(current.getData().equals(hash)) {
				return current.getIndex();
			}
			if(current.getLeft() != null) {
				q.add(current.getLeft());
			}
			if(current.getRight() != null) {
				q.add(current.getRight());
			}
		}
		return -1;
	}
	
	public static int realIndex(int hashIndex,int totalLeaves) {
		int current = totalLeaves;
		int sumNodes = 0;
		while(current != 1) {
			if(current %2 == 1) {
				sumNodes += (current+1)/2;
				current = (current+1)/2;
			} else {
				sumNodes += current/2;
				current = current/2;
			}
		}
		
		return hashIndex-sumNodes-1;
	}
}
