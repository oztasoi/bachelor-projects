package deposit;

/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class Node extends Coordinate {

	/**
	 * the next node field
	 */
	private Node next;
	
	/**
	 * the simple constructor
	 */
	
	public Node() {
		
		super();
		this.next = null;
	}
	
	/**
	 * the constructor with nextNode parameter
	 * @param nextNode shows the next node of this node.
	 */
	public Node(Node nextNode) {
		super();
		this.next = nextNode;
		
	}
	
	/**
	 * the constructor with current coordinate.
	 * @param coordinate shows the current coordinate of this node.
	 */
	public Node(Coordinate coordinate) {
		super(coordinate.x, coordinate.y);
		this.next = null;
		
	}
	
	/**
	 * the advanced constructor with 2 parameters
	 * @param coordinate shows the current coordinate of this node.
	 * @param nextNode shows the next node of this node.
	 */
	public Node(Coordinate coordinate, Node nextNode) {
		super(coordinate.x, coordinate.y);
		this.next = nextNode;
		
	}

	/**
	 * getter of nextNode.
	 * @return nextNode
	 */
	public Node getNext() {
		return next;
	}

	/**
	 * setter of nextNode.
	 * @param next nextNode of this node.
	 */
	public void setNext(Node next) {
		this.next = next;
	}
	
}
