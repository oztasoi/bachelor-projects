package deposit;

/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class Coordinate {
	/**
	 * x value of the coordinate
	 */
	public int x; 
	/**
	 * y value of the coordinate
	 */
	public int y;
	
	/**
	 * simple constructor when there is no parameter.
	 */
	public Coordinate() {
		this.x = 0;
		this.y = 0;
		
	}
	
	/**
	 * 
	 * @param x the value of the x component
	 * @param y the value of the y component
	 */
	public Coordinate(int x, int y) {
		this.x = x;
		this.y = y;
		
	}
	
	

}
