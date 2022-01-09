package deposit;

import java.awt.Color;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

import environment.Action;
import environment.Action.Type;
import environment.LocalInformation;
import game.Direction;
import game.Drawable;
import ui.GridPanel;

/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class Snake implements Drawable {

	/**
	 * the LinkedList of the snake's nodes. 
	 */
	public List<Node> mySnake;
	
	/**
	 * the unique color value of the snake.
	 */
	public Color color;

	/**
	 * simple constructor of the snake. It is used only once in the project at the beginning.
	 */
	public Snake() {
		mySnake = new LinkedList<Node>();
		mySnake.add(new Node(new Coordinate(4, 1)));
		mySnake.add(new Node(new Coordinate(3, 1)));
		mySnake.add(new Node(new Coordinate(2, 1)));
		mySnake.add(new Node(new Coordinate(1, 1)));
		color = new Color((int)(Math.random()*150+55),(int)(Math.random()*150+55),(int)(Math.random()*150+55));

	}

	/**
	 * the regular constructor that takes a LinkedList and creates a Snake.
	 * @param parameterList the parameter list that is sent by the reproduce() method.
	 */
	public Snake(List<Node> parameterList) {

		mySnake = parameterList;
		color = new Color((int)(Math.random()*150+55),(int)(Math.random()*150+55),(int)(Math.random()*150+55));
	}

	/**
	 * the main action method that represents a very simple AI.
	 * @param localInformation takes the localInformation of this Snake and acts the current situation.
	 * @return new Action which is needed.
	 */
	public Action chooseAction(LocalInformation localInformation) {
		if (this.mySnake.size() == 8) {
			return new Action(Type.REPRODUCE);
		} else if (isAbleToEat(localInformation.getBait())) {
			return new Action(Type.EAT);
		} else {
			Direction d = bestWayToGo(localInformation);
			if (d != null) {
				return new Action(Type.MOVE, d);
			} else {
				return new Action(Type.STAY);
			}
		}

	}

//	public void bfsMove() {
//		/*
//		 * have an empty list
//		 * send the snake's head.
//		 * 
//		 * 
//		 * add the possible adjacent unvisited values to the list.
//		 * at each element in the list until the list is empty, do the same thing for them
//		 * until the destination is reached.
//		 * 
//		 * 
//		 * btw create a stack for backtracking.
//		 */
//	}
	
	/**
	 * the smart move method that helps the snake to find its own path.
	 * But it is very simple and has no regular path-finding algorithm. It should be improved.
	 * @param localInformation localInformation of this snake
	 * @return Direction of which is more sensible.
	 */
	public Direction bestWayToGo(LocalInformation localInformation) {

		Bait myLovelyBait = localInformation.getBait();
		HashMap<Direction, Integer> directionValues = localInformation.getDirectionValues();
		Node headNode = this.mySnake.get(0);
		

		if (myLovelyBait.x > headNode.x) {
			if (directionValues.get(Direction.RIGHT) == 0) {
				return Direction.RIGHT;
			}
		}
		if (myLovelyBait.x < headNode.x) {
			if (directionValues.get(Direction.LEFT) == 0) {
				return Direction.LEFT;
			}
		}
		if (myLovelyBait.y > headNode.y) {
			if (directionValues.get(Direction.DOWN) == 0) {
				return Direction.DOWN;
			}
		}
		if (myLovelyBait.y < headNode.y) {
			if (directionValues.get(Direction.UP) == 0) {
				return Direction.UP;
			}
		}
		
		List<Direction> freeDirectionsList = localInformation.getFreeDirections();

		if (!freeDirectionsList.isEmpty()) {
			Direction d = LocalInformation.getRandomDirection(freeDirectionsList);
 			return d;
		}

		return null;

	}

	/**
	 * checks if the snake is able to eat the bait.
	 * @param b the current bait.
	 * @return the boolean value of the action(true or false).
	 */
	public boolean isAbleToEat(Bait b) {
		Node headNode = this.mySnake.get(0);
		return ((headNode.x == b.x && headNode.y - b.y == 1) || (headNode.x == b.x && headNode.y - b.y == -1)
				|| (headNode.y == b.y && headNode.x - b.x == 1) || (headNode.y == b.y && headNode.x - b.x == -1));
	}

	/**
	 * the reproduction method that creates a new Snake.
	 * @return a new Snake with the needed information.
	 */
	public Snake reproduce() {
		List<Node> mySnakeCopy = new LinkedList<Node>();
		Node currentNode;
		for (int i = 1; i < 5; i++) {
			currentNode = mySnake.get(mySnake.size() - 1);
			mySnakeCopy.add(new Node(new Coordinate(currentNode.x, currentNode.y)));
			mySnake.remove(currentNode);
		}

		return new Snake(mySnakeCopy);
	}

	/**
	 * the eat method/
	 * @param b the bait.
	 */
	public void eat(Bait b) {
		mySnake.add(0, b);
	}

	/**
	 * the move method that takes a Direction and moves towards it.
	 * @param direction the given direction.
	 */
	public void move(Direction direction) {
		Node headNode = this.mySnake.get(0);
		if (direction == Direction.DOWN) {
			mySnake.add(0, new Node(new Coordinate(headNode.x, headNode.y + 1)));
			mySnake.remove(mySnake.size() - 1);
		} else if (direction == Direction.UP) {
			mySnake.add(0, new Node(new Coordinate(headNode.x, headNode.y - 1)));
			mySnake.remove(mySnake.size() - 1);
		} else if (direction == Direction.LEFT) {
			mySnake.add(0, new Node(new Coordinate(headNode.x - 1, headNode.y)));
			mySnake.remove(mySnake.size() - 1);
		} else {
			mySnake.add(0, new Node(new Coordinate(headNode.x + 1, headNode.y)));
			mySnake.remove(mySnake.size() - 1);
		}
	}

	/**
	 * the staying method when all else fails.
	 */
	public void stay() {
		Node headNode = this.mySnake.get(0);
		mySnake.add(0, new Node(new Coordinate(headNode.x, headNode.y)));
		mySnake.remove(0);
	}

	@Override
	public void draw(GridPanel panel) {
		panel.drawSquare(mySnake.get(0).x, mySnake.get(0).y, Color.RED);
		for (int i = 1; i < mySnake.size(); i++) {
			Node temporary = mySnake.get(i);
			panel.drawSquare(temporary.x, temporary.y, color);
		}
	}
}
