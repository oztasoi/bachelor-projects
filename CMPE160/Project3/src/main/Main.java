package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Stack;

import project.MerkleTree;
import project.Utility;

public class Main {

	public static void main(String[] args) throws NoSuchAlgorithmException, IOException{
		
		
		try {
			MerkleTree m0 = new MerkleTree("data/1_bad.txt");		
			String hash = m0.getRoot().getLeft().getRight().getData();
			System.out.println(hash);
			boolean valid = m0.checkAuthenticity("data/1meta.txt");
			System.out.println(valid);

			
			//The following just is an example for you to see the usage. 
			//Although there is none in reality, assume that there are two corrupt chunks in this example.
			ArrayList<Stack<String>> corrupts = m0.findCorruptChunks("data/1meta.txt");
			System.out.println("Corrupt hash of first corrupt chunk is: " + corrupts.get(0).pop());
			//System.out.println("Corrupt hash of second corrupt chunk is: " + corrupts.get(1).pop());

			download("secondaryPart/data/download_from_trusted.txt");
			
		} catch (IndexOutOfBoundsException e) {
			System.out.println("There is no more than 1 corrupted chunk.");
		} catch (FileNotFoundException q) {
			System.out.println("Take me to church.");
		}
	}

	public static void download(String path) throws IOException, NoSuchAlgorithmException {
		// Entry point for the secondary part
		FileReader f = new FileReader(new File(path));
		Scanner sc = new Scanner(f);
		ArrayList<String> list = new ArrayList<String>();
		while(sc.hasNext()) {
				list.add(sc.next());
		}
		sc.close();
		for(int i=0; i<list.size(); i++) {
			if(i%3 == 0) {
				String s = list.get(i);
				Utility.metaGenerator(s);
			} else if(i%3 == 1) {
				String s = list.get(i);
				URL u1 = new URL(s);
				Scanner a = new Scanner(new InputStreamReader(u1.openStream()));
				File dirs;
				(dirs = new File("secondaryPart/data/split/"+Utility.nameGenerator(s))).mkdirs();
				
				File qt = new File(dirs+"/"+Utility.nameGenerator(s)+".txt");
				PrintStream ps = new PrintStream(qt);
				int j = 0;
				while(a.hasNext()) {
					URL url = new URL(a.next());
					InputStream in = url.openStream();
					String filename;
					if(j<10) {
						filename = "0"+j;
					} else {
						filename = j + "";
					}
					ps.println(dirs+"\\"+filename);
					File file = new File(dirs, filename);
//					inspired from the link :  "https://stackoverflow.com/questions/20265740/how-to-download-a-pdf-from-a-given-url-in-java"
					Files.copy(in, Paths.get(dirs + File.separator + file.getName()),
							StandardCopyOption.REPLACE_EXISTING);
					in.close();
					j++;
				}
				a.close();
				ps.close();
				
				String treepath = "secondaryPart/data/split/"+Utility.nameGenerator(s)+"/"+Utility.nameGenerator(s)+".txt";
				String metapath = "secondaryPart/"+Utility.nameGenerator(s)+"meta.txt";
				
				MerkleTree tree0 = new MerkleTree(treepath);
				
				if(!tree0.checkAuthenticity(metapath)) {
					ArrayList<Stack<String>> corruptedStacks = tree0.findCorruptChunks(metapath);
					while(!corruptedStacks.isEmpty()) {
						String corruptedHash = corruptedStacks.get(0).pop();
						System.out.println("file" + Utility.nameGenerator(s) + "has corrupted chunks." );
						System.out.println(corruptedHash);
						int metaIndex = Utility.bfsTraversal(corruptedHash, tree0.getRoot());
						int leafIndex = Utility.realIndex(metaIndex, j);
						System.out.println(leafIndex);
						String alternativelink = list.get(i+1);
						URL alternative = new URL(alternativelink);
						Scanner alternativescanner = new Scanner(new InputStreamReader(alternative.openStream()));
						int assistantcounter = 0;
						while(assistantcounter<leafIndex) {
							alternativescanner.next();
							assistantcounter++;
						}
						String alternativechunk = alternativescanner.next();
						URL alternativechunklink = new URL(alternativechunk);
						InputStream in = alternativechunklink.openStream();
						String leafIndexString;
						if(leafIndex < 10) {
							leafIndexString = "0" + leafIndex;
						} else {
							leafIndexString = leafIndex + "";
						}
						File file = new File("secondaryPart/data/split/"+Utility.nameGenerator(s)+"/"+leafIndexString);
						Files.copy(in, Paths.get(dirs + File.separator + file.getName()),
								StandardCopyOption.REPLACE_EXISTING);
						corruptedStacks.remove(0);
						alternativescanner.close();
					}
				}
				
				File dir = new File("secondaryPart/data/split/" + Utility.nameGenerator(s));
				File output = new File("secondaryPart/data/split/"+Utility.nameGenerator(s)+"/output"+Utility.nameGenerator(s)+".jpg");
				
				Utility.jpegMerge(dir, output);
				
			}
		}
	}


}