package project;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;

import util.HashGeneration;

public class MerkleTree {

	public class MNode {

		private int index;

		private String hash;

		private File directedFile;

		private MNode left;
		private MNode right;

		public MNode() {
			this.index = 0;
			this.hash = "";
			this.directedFile = null;
			this.left = null;
			this.right = null;
		}

		public MNode(String path) throws NoSuchAlgorithmException, IOException {
			this.index = 0;
			this.directedFile = new File(path);
			this.hash = HashGeneration.generateSHA256(directedFile);
			this.left = null;
			this.right = null;
		}

		public String getData() {
			return hash;
		}

		public MNode getLeft() {
			return left;
		}

		public MNode getRight() {
			return right;
		}
		
		public int getIndex() {
			return index;
		}

		public File getDirectedFile() {
			return directedFile;
		}
	}

	private MNode root;

	public MNode getRoot() {
		return this.root;
	}

	public MerkleTree(String path) throws NoSuchAlgorithmException, IOException {
		MerkleTreeConstructor(path);
	}

	private void MerkleTreeConstructor(String path) throws NoSuchAlgorithmException, IOException {
		ArrayList<MNode> nodeData = fileListCreator(path);
		int level = levelCalculator(nodeData);
		root = TreeConstructor(nodeData, level);
		indexOptimizer(root);
	}

	private ArrayList<MNode> fileListCreator(String path) throws NoSuchAlgorithmException, IOException {
		Scanner sc = new Scanner(new File(path));
		String s = "";
		ArrayList<MNode> nodeData = new ArrayList<MNode>();
		while (sc.hasNextLine()) {
			s = sc.nextLine();
			nodeData.add(new MNode(s));
		}
		sc.close();
		return nodeData;
	}

	private int levelCalculator(ArrayList<MNode> nodeData) {
		int size = nodeData.size();
		int level = 0;
		while (size > 1) {
			level += 1;
			size /= 2;
		}

		return level + 1;
	}

	private void indexOptimizer(MNode root) {

		Queue<MNode> q = new LinkedList<MNode>();
		int i = 1;
		q.add(root);
		while (!q.isEmpty()) {
			MNode temp = q.poll();
			temp.index = i;
			if (temp.left != null) {
				q.add(temp.left);
			}
			if (temp.right != null) {
				q.add(temp.right);
			}
			i++;
		}
	}

	private MNode TreeConstructor(ArrayList<MNode> nodeData, int level)
			throws NoSuchAlgorithmException, UnsupportedEncodingException {
		Queue<MNode> q = new LinkedList<MNode>();
		int minlevel = 0;
		while (level > minlevel) {
			if (nodeData.size() != 1) {
				if (nodeData.size() % 2 == 1) {
					int rep = nodeData.size() / 2;
					for (int i = 0; i < rep; i++) {
						q.add(nodeData.remove(0));
						q.add(nodeData.remove(0));
						MNode parent = new MNode();
						parent.left = q.poll();
						parent.right = q.poll();
						parent.hash = HashGeneration.generateSHA256(parent.left.hash + parent.right.hash);
						nodeData.add(parent);
					}
					MNode lastOne = nodeData.remove(0);
					MNode parent = new MNode();
					parent.left = lastOne;
					parent.hash = HashGeneration.generateSHA256(parent.left.hash + "");
					nodeData.add(parent);
				} else {
					int rep = nodeData.size() / 2;
					for (int i = 0; i < rep; i++) {
						q.add(nodeData.remove(0));
						q.add(nodeData.remove(0));
						MNode parent = new MNode();
						parent.left = q.poll();
						parent.right = q.poll();
						parent.hash = HashGeneration.generateSHA256(parent.left.hash + parent.right.hash);
						nodeData.add(parent);
					}
				}
			}
			level--;
		}
		return nodeData.get(0);
	}

	public boolean checkAuthenticity(String path) throws FileNotFoundException {
		Scanner sc = new Scanner(new File(path));
		String s = sc.nextLine();
		sc.close();
		return root.hash.equals(s);
	}

	public HashMap<Integer, String> metamap(String path) throws FileNotFoundException {
		Scanner sc = new Scanner(new File(path));
		HashMap<Integer, String> meta = new HashMap<Integer, String>();
		int i = 1;
		while (sc.hasNextLine()) {
			meta.put(i, sc.nextLine());
			i++;
		}
		sc.close();
		return meta;
	}

	public ArrayList<Stack<String>> findCorruptChunks(String path) throws FileNotFoundException {
		HashMap<Integer, String> metadata = metamap(path);
		ArrayList<Stack<String>> corruptChunks = new ArrayList<Stack<String>>();
		Stack<String> mystack = new Stack<String>();
		corrupted(corruptChunks, metadata, mystack, root);
		return corruptChunks;
	}

	private void corrupted(ArrayList<Stack<String>> corruptChunks, HashMap<Integer, String> metadata,
			Stack<String> mystack, MNode current) {
		if (current.left == null && current.right == null) {
			if (!current.hash.equals(metadata.get(current.index))) {
				mystack.add(current.hash);
				corruptChunks.add(mystack);
			}
		} else {
			if (current.left != null && current.right != null) {
				if (!current.left.hash.equals(metadata.get(current.left.index))
						&& current.right.hash.equals(metadata.get(current.right.index))) {
					mystack.add(current.hash);
					corrupted(corruptChunks, metadata, mystack, current.left);
				} else if (current.left.hash.equals(metadata.get(current.left.index))
						&& !current.right.hash.equals(metadata.get(current.right.index))) {
					mystack.add(current.hash);
					corrupted(corruptChunks, metadata, mystack, current.right);
				} else {
					mystack.add(current.hash);
					@SuppressWarnings("unchecked")
					Stack<String> temp = ((Stack<String>) mystack.clone());
					corrupted(corruptChunks, metadata, mystack, current.left);
					corrupted(corruptChunks, metadata, temp, current.right);
				}
			} else if (current.right == null) {

				mystack.add(current.hash);
				corrupted(corruptChunks, metadata, mystack, current.left);

			}
		}
	}
}
