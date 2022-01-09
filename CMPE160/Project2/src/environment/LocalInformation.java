package environment;

import java.util.HashMap;
import java.util.List;

import deposit.Bait;
import deposit.Coordinate;
import game.Direction;

/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class LocalInformation {

	/**
	 * the width of the game grid.
	 */
	private int gridWidth;
	/**
	 * the height of the game height.
	 */
	private int gridHeight;

	/**
	 * the current bait.
	 */
	private Bait bait;
	
	/**
	 * the current situation of the map.
	 */
	private int[][] binaryMap;

	/**
	 * the hash map of the directions and its values according to the map.
	 */
	private HashMap<Direction, Integer> destination;
	/**
	 * the current snakes' locations on the map.
	 */
	private List<Coordinate> currentLocation;
	/**
	 * the list of current directions of the snake's head.
	 */
	private List<Direction> freeDirections;

	/**
	 * the current constructor.
	 * @param gridWidth map's width.
	 * @param gridHeight map's height.
	 * @param destination snake's sensible free directions towards the bait.
	 * @param bait the current bait.
	 * @param binaryMap the current situation of the map.
	 * @param currentLocation the current location of the snake.
	 * @param freeDirections all current free directions.
	 */
	LocalInformation(int gridWidth, int gridHeight, HashMap<Direction, Integer> destination, Bait bait, int[][] binaryMap,
			List<Coordinate> currentLocation, List<Direction> freeDirections) {
		this.gridWidth = gridWidth;
		this.gridHeight = gridHeight;
		this.bait = bait;
		this.binaryMap = binaryMap;
		this.destination = destination;
		this.currentLocation = currentLocation;
		this.freeDirections = freeDirections;
	}

	/**
	 * getter method of the gridWidth.
	 * @return gridWidth.
	 */
	public int getGridWidth() {
		return gridWidth;
	}

	/**
	 * getter method of the gridHeight.
	 * @return gridHeight.
	 */
	public int getGridHeight() {
		return gridHeight;
	}

	/**
	 * getter method of the value of the direction.
	 * @return 0 or 1
	 */
	public Integer getIntegerUp() {
		return destination.get(Direction.UP);
	}
	
	/**
	 * getter method of the value of the direction.
	 * @return 0 or 1
	 */
	public Integer getIntegerDown() {
		return destination.get(Direction.DOWN);
	}

	/**
	 * getter method of the value of the direction.
	 * @return 0 or 1
	 */
	public Integer getIntegerLeft() {
		return destination.get(Direction.LEFT);
	}

	/**
	 * getter method of the value of the direction.
	 * @return 0 or 1
	 */
	public Integer getIntegerRight() {
		return destination.get(Direction.RIGHT);
	}

	/**
	 * getter method of the freeDirections list
	 * @return freeDirections
	 */
	public List<Direction> getFreeDirections() {
		return freeDirections;
	}

	/**
	 * getter method of the current bait.
	 * @return the bait.
	 */
	public Bait getBait() {
		return this.bait;
	}
	
	/**
	 * getter method of the current location of the snake.
	 * @return the currentLocation.
	 */
	public List<Coordinate> getLocation(){
		return this.currentLocation;
	}
	
	/**
	 * getter method of the direction values' hash map.
	 * @return the HashMap 
	 */
	public HashMap<Direction, Integer> getDirectionValues(){
		return this.destination;
	}
	
	/**
	 * getter method of the current situation of the map.
	 * @return the current situation of the map
	 */
	public int[][] getBinaryMap(){
		return this.binaryMap;
	}

	/**
	 * getter method of a random direction of the freeDirections list
	 * @param possibleDirections the possible directions' list.
	 * @return Direction
	 */
	public static Direction getRandomDirection(List<Direction> possibleDirections) {
		if (possibleDirections.isEmpty()) {
			return null;
		}
		int randomIndex = (int) (Math.random() * possibleDirections.size());
		return possibleDirections.get(randomIndex);
	}

}
