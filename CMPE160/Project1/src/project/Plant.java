package project;

import java.awt.Color;
import java.util.List;

import game.Direction;
import naturesimulator.Action;
import naturesimulator.Action.Type;
import naturesimulator.LocalInformation;
import ui.GridPanel;

/**
 * Specialized class that extends Creature and the main life form of Herbivore to keep alive.
 * @author Ozgurcan Oztas
 *
 */
public class Plant extends Creature {

	/**
	 * 	 * the value of maximum life point that a Plant can ever achieve.
	 */
	private static final double MAX_HEALTH = 1.0;

	/**
	 * General constructor of the Plant that takes parameters _x and _y as components of the coordinate.
	 * @param _x the x component of the coordinate of the plant.
	 * @param _y the y component of the coordinate of the plant.
	 */
	public Plant(int _x, int _y) {
		super(_x, _y);
		this.setHealth(MAX_HEALTH * 0.5);

	}

	/**
	 * Specialized constructor of the Plant that takes parameters _x and _y as components of the coordinate.
	 * Also takes parameter parameterHealth to initially set its life points to the parameterHealth. Used @method reproduce.
	 * @param _x the x component of the coordinate of the plant.	
	 * @param _y the y component of the coordinate of the plant.
	 * @param parameterHealth the numerical value that corresponds the life point of the plant.
	 */
	public Plant(int _x, int _y, double parameterHealth) {
		super(_x, _y);
		this.setHealth(parameterHealth);
	}

	/**
	 * general method of drawing at the layout in the simulator. 
	 * Draws different colors of squares depends on the life point of the Plant.
	 * Takes GridPanel as a parameter to draw a square on the panel.
	 * @param panel the drawing panel to draw appropriate squares according to the life point of the plant.
	 */
	@Override
	public void draw(GridPanel panel) {
		if (this.getHealth() <= 0.5) {
			panel.drawSquare(getX(), getY(), new Color(0, 255, 0));
		} else if (this.getHealth() > 0.5 && this.getHealth() <= 0.75) {
			panel.drawSquare(getX(), getY(), new Color(0, 185, 0));
		} else {
			panel.drawSquare(getX(), getY(), new Color(0, 115, 0));
		}
	}

	/**
	 * Specialized conception of the Herbivore that takes LocalInformation as a parameter and returns a valid action.
	 * There may be two outcomes which are either Reproduce or Stay.
	 * @param localInformation the information of the Plant includes the information of its surroundings.
	 * @return new Action(Type.type, Direction direction), new Action(Type.type);
	 */
	@Override
	public Action chooseAction(LocalInformation localInformation) {

		List<Direction> listDirection = localInformation.getFreeDirections();
		Direction directionReproduce = LocalInformation.getRandomDirection(listDirection);

		if (this.getHealth() >= Plant.MAX_HEALTH * 0.75 && directionReproduce != null) {
			return new Action(Type.REPRODUCE, directionReproduce);
		} else {
			return new Action(Type.STAY);
		}
	}

	/**
	 * specialized method of Plant that manages to reproduce action. 
	 * Takes a Direction as a parameter and returns a new Plant with the suitable properties.
	 * @param direction the suitable direction(s) to reproduce.
	 * @return new Plant(Integer _x, Integer _y, double parameterHealth);
	 */
	@Override
	public Plant reproduce(Direction direction) {

		this.setHealth(getHealth() * 0.7);
		if (direction == Direction.DOWN) {
			return new Plant(this.getX(), this.getY() + 1, getHealth() / 7.0);
		} else if (direction == Direction.UP) {
			return new Plant(this.getX(), this.getY() - 1, getHealth() / 7.0);
		} else if (direction == Direction.RIGHT) {
			return new Plant(this.getX() + 1, this.getY(), getHealth() / 7.0);
		} else {
			return new Plant(this.getX() - 1, this.getY(), getHealth() / 7.0);
		}
	}

	/**
	 * specialized method of Plant that is a short-brief version of photosynthesis.
	 * Allows Plant to increase its health each time it is called.
	 */
	@Override
	public void stay() {
		this.setHealth(getHealth() + 0.05);
		if (this.getHealth() >= MAX_HEALTH) {
			this.setHealth(MAX_HEALTH);
			return;
		}
	}

}
