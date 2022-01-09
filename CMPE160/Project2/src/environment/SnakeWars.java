package environment;

import game.Direction;
import game.GridGame;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

import deposit.Bait;
import deposit.Coordinate;
import deposit.Node;
import deposit.Snake;

/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class SnakeWars extends GridGame {

	/**
	 * the list of snakes in the game.
	 */
	private List<Snake> snakeList;
	/**
	 * the game map.
	 */
	private int[][] positionMap;
	/**
	 * the bait in the game.
	 */
	private Bait myLovelyBait;
	/**
	 * the random object that helps in the game regulation.
	 */
	private final Random rand = new Random();

	/**
	 * the current constructor of the game.
	 * @param gridWidth width of the game.
	 * @param gridHeight height of the game.
	 * @param gridSquareSize the size of the square in the gameGrid.
	 * @param frameRate the rate of the change in frames per second.
	 */
	public SnakeWars(int gridWidth, int gridHeight, int gridSquareSize, int frameRate) {

		super(gridWidth, gridHeight, gridSquareSize, frameRate);

		snakeList = new ArrayList<Snake>();
		positionMap = new int[getGridWidth()][getGridHeight()];
		clearMap();
		addSnake(new Snake());
		myLovelyBait = baitGenerator(snakeList.get(0));
		addDrawable(myLovelyBait);

	}

	@Override
	protected void timerTick() {

		ArrayList<Snake> snakeListCopy = new ArrayList<Snake>(snakeList);

		// For each snake
		for (Snake snake : snakeListCopy) {

			// Reset the place

			Node headNode = snake.mySnake.get(0);
			Action action = snake.chooseAction(createLocalInformationForSnake(snake));
			uptadeMap(snake, 0);

			if (action != null) {
				if (action.getType() == Action.Type.STAY) {
					snake.stay();
				} else if (action.getType() == Action.Type.REPRODUCE) {
					Snake newSnake = snake.reproduce();
					addSnake(newSnake);
				} else if (action.getType() == Action.Type.EAT && snake.isAbleToEat(myLovelyBait)) {
					snake.eat(myLovelyBait);
					removeDrawable(myLovelyBait);
					myLovelyBait = baitGenerator(snake);
					addDrawable(myLovelyBait);
				} else if (action.getType() == Action.Type.MOVE) {
					if (isDirectionFree(headNode.x, headNode.y, action.getDirection())) {
						snake.move(action.getDirection());

					}
				}
			}
			uptadeMap(snake, 1);
		}
	}

	/**
	 * checker method whether the direction is available or not.
	 * @param x current x coordinate.
	 * @param y current y coordinate.
	 * @param direction desired direction.
	 * @return true or false.
	 */
	private boolean isDirectionFree(int x, int y, Direction direction) {

		if (direction == null) {
			return false;
		}

		int xTarget = x;
		int yTarget = y;

		if (direction == Direction.UP) {
			yTarget--;
		} else if (direction == Direction.DOWN) {
			yTarget++;
		} else if (direction == Direction.LEFT) {
			xTarget--;
		} else if (direction == Direction.RIGHT) {
			xTarget++;
		}

		return isPositionFree(xTarget, yTarget);
	}

	/**
	 * checks the position whether it is free or not.
	 * @param xTarget desired x coordinate.
	 * @param yTarget desired y coordinate.
	 * @return true or false.
	 */
	private boolean isPositionFree(int xTarget, int yTarget) {

		return isPositionInsideGrid(xTarget, yTarget) && getValueAtPosition(xTarget, yTarget) == 0;
	}

	/**
	 * checks the position whether inside the grid or not.
	 * @param xTarget desired x location.
	 * @param yTarget desired y location.
	 * @return true or false.
	 */
	private boolean isPositionInsideGrid(int xTarget, int yTarget) {

		return (xTarget >= 0 && xTarget < getGridWidth()) && (yTarget >= 0 && yTarget < getGridHeight());
	}

	/**
	 * checks the position of its value.
	 * @param xTarget desired x location.
	 * @param yTarget desired y location.
	 * @return 0 or 1.
	 */
	private int getValueAtPosition(int xTarget, int yTarget) {
		if (isPositionInsideGrid(xTarget, yTarget)) {
			return positionMap[xTarget][yTarget];
		} else {
			return 1;
		}
	}

	/**
	 * adder method that adds snake into the snakeList.
	 * @param newSnake newly born snake.
	 */
	private void addSnake(Snake newSnake) {
		Node currentNode;
		for (int i = 0; i < newSnake.mySnake.size(); i++) {
			currentNode = newSnake.mySnake.get(i);
			positionMap[currentNode.x][currentNode.y] = 1;

		}
		snakeList.add(newSnake);
		addDrawable(newSnake);

	}

	/**
	 * the bait generator in the game.
	 * @param snake takes the snake's current position.
	 * @return a new Bait at a location which is empty.
	 */
	private Bait baitGenerator(Snake snake) {
		List<Coordinate> currentSnake = snakePosition(snake);
		int[][] binaryMapCopy = positionMap;
		for(int i=0;i<currentSnake.size();i++) {
			binaryMapCopy[currentSnake.get(i).x][currentSnake.get(i).y] = 1;
		}
		int xCoord, yCoord;
		do {
			xCoord = rand.nextInt(getGridWidth());
			yCoord = rand.nextInt(getGridHeight());
		} while (binaryMapCopy[xCoord][yCoord] == 1);
		positionMap[xCoord][yCoord] = 5;
		return new Bait(new Coordinate(xCoord, yCoord));
	}

	/**
	 * creator method of LocalInformation of the current Snake.
	 * @param snake current snake.
	 * @return LocalInformation.
	 */
	private LocalInformation createLocalInformationForSnake(Snake snake) {

		List<Coordinate> position = snakePosition(snake);
		Node headNode = snake.mySnake.get(0);

		int x = headNode.x;
		int y = headNode.y;

		HashMap<Direction, Integer> directionValues = new HashMap<Direction, Integer>();
		directionValues.put(Direction.DOWN, getValueAtPosition(x, y + 1));
		directionValues.put(Direction.UP, getValueAtPosition(x, y - 1));
		directionValues.put(Direction.LEFT, getValueAtPosition(x - 1, y));
		directionValues.put(Direction.RIGHT, getValueAtPosition(x + 1, y));

		ArrayList<Direction> freeDirections = new ArrayList<>();
		if (directionValues.get(Direction.DOWN) == 0 && isPositionInsideGrid(x, y + 1)) {
			freeDirections.add(Direction.DOWN);
		} else if (directionValues.get(Direction.UP) == 0 && isPositionInsideGrid(x, y - 1)) {
			freeDirections.add(Direction.UP);
		} else if (directionValues.get(Direction.LEFT) == 0 && isPositionInsideGrid(x - 1, y)) {
			freeDirections.add(Direction.LEFT);
		} else if (directionValues.get(Direction.RIGHT) == 0 && isPositionInsideGrid(x + 1, y)) {
			freeDirections.add(Direction.RIGHT);
		}

		return new LocalInformation(getGridWidth(), getGridHeight(), directionValues, myLovelyBait, positionMap, position,
				freeDirections);
	}

	/**
	 * clears the map just for one time at the beginning of the game.
	 */
	private void clearMap() {
		for (int i = 0; i < getGridWidth(); i++) {
			for (int j = 0; j < getGridHeight(); j++) {
				positionMap[i][j] = 0;
			}
		}
	}

	/**
	 * Update method of the map that updates the map by a given value.
	 * @param snake current snake.
	 * @param value desired value.
	 */
	private void uptadeMap(Snake snake, int value) {
		Node currentNode;
		for (int i = 0; i < snake.mySnake.size(); i++) {
			currentNode = snake.mySnake.get(i);
			positionMap[currentNode.x][currentNode.y] = value;
		}
	}

	/**
	 * creates the current snake's current locations as a list.
	 * @param snake current snake
	 * @return List<Coordinate>
	 */
	private List<Coordinate> snakePosition(Snake snake) {
		List<Coordinate> position = new ArrayList<Coordinate>();
		Node currentNode;
		for (int i = 0; i < snake.mySnake.size(); i++) {
			currentNode = snake.mySnake.get(i);
			position.add(new Coordinate(currentNode.x, currentNode.y));
		}

		return position;
	}

}