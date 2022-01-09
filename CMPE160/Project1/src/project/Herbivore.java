package project;

import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import game.Direction;
import naturesimulator.Action;
import naturesimulator.Action.Type;
import naturesimulator.LocalInformation;
import ui.GridPanel;

/**
 * Specialized class that extends Creature and the plant predator of the simulator.
 * @author Ozgurcan Oztas
 *
 */
public class Herbivore extends Creature {

	
	/**
	 * the value of maximum life point that a Herbivore can ever achieve.
	 */
	private final double MAX_HEALTH = 20.0;

	
	/**
	 * general constructor of the Herbivore that takes _x and _y as the components of coordinate.
	 * @param _x the x component of the coordinate of the Herbivore.
	 * @param _y the y component of the coordinate of the Herbivore.
	 */
	public Herbivore(int _x, int _y) {
		super(_x, _y);
		this.setHealth(MAX_HEALTH*0.5);
	}

	/**
	 * special constructor of the Herbivore that takes _x and _y as the components of the coordinate and also takes 
	 * parameterHealth to initially set its life points to that variable. Used @method reproduce.
	 * @param _x the x component of the coordinate of the Herbivore.
	 * @param _y the y component of the coordinate of the Herbivore.
	 * @param parameterHealth the numerical value that corresponds to the life point of Herbivore.
	 */
	public Herbivore(int _x, int _y, double parameterHealth) {
		super(_x, _y);
		this.setHealth(parameterHealth);
	}

	/**
	 * general method of drawing at the layout in the simulator. 
	 * Draws different colors of squares depends on the life point of the Herbivore.
	 * Takes GridPanel as a parameter to draw a square on the panel.
	 * @param panel the drawing panel to draw appropriate squares according to the life point of Herbivore.
	 */
	@Override
	public void draw(GridPanel panel) {
		if (this.getHealth() < MAX_HEALTH * 0.5) {
			panel.drawSquare(getX(), getY(), new Color(255, 0, 0));
		} else if (this.getHealth() >= MAX_HEALTH * 0.5 && this.getHealth() < MAX_HEALTH * 0.75) {
			panel.drawSquare(getX(), getY(), new Color(185, 0, 0));
		} else {
			panel.drawSquare(getX(), getY(), new Color(75, 0, 0));
		}
	}

	/**
	 * Specialized conception of the Herbivore that takes LocalInformation as a parameter and returns a valid action.
	 * There may be four outcomes which are Reproduce, Attack, Move and Stay.
	 * @param localInformation the information of the Herbivore includes the information of its surroundings.
	 * @return new Action(Type.type, Direction direction), new Action(Type.type, Creature creature), new Action(Type.type);
	 */
	@Override
	public Action chooseAction(LocalInformation localInformation) {
		List<Direction> listDirection = localInformation.getFreeDirections();
		Direction directionReproduce = LocalInformation.getRandomDirection(listDirection);

		if (this.getHealth() == MAX_HEALTH && directionReproduce != null) {
			return new Action(Type.REPRODUCE, directionReproduce);
		} else if (findThePrey(localInformation) != null) {
			return new Action(Type.ATTACK, findThePrey(localInformation));
		} else if (directionReproduce != null && this.getHealth()>1.0) {
			return new Action(Type.MOVE, directionReproduce);
		} else {
			return new Action(Type.STAY);
		}
	}

	/**
	 * specialized method of Herbivore that manages to reproduce action. 
	 * Takes a Direction as a parameter and returns a new Herbivore with the suitable properties.
	 * @param direction the suitable direction(s) to reproduce.
	 * @return new Herbivore(Integer _x, Integer _y, double parameterHealth);
	 */
	@Override
	public Creature reproduce(Direction direction) {
		this.setHealth(getHealth()*0.4);
		if (direction == Direction.DOWN) {
			return new Herbivore(this.getX(), this.getY() + 1, this.getHealth()*0.5);
		} else if (direction == Direction.UP) {
			return new Herbivore(this.getX(), this.getY() - 1, this.getHealth()*0.5);
		} else if (direction == Direction.LEFT) {
			return new Herbivore(this.getX() - 1, this.getY(), this.getHealth()*0.5);
		} else{
			return new Herbivore(this.getX() + 1, this.getY() , this.getHealth()*0.5);
		}
	}

	/**
	 * specialized method of Herbivore that attacks to another Creature.
	 * Takes a Creature as a parameter and siphons its life points, hence the attacked creature has no life points.
	 * @param attackedCreature the suitable target to attack.
	 */
	public void attack(Creature attackedCreature) {
		this.setHealth(getHealth()+attackedCreature.getHealth());
		attackedCreature.setHealth(0.0);
		if (this.getHealth() >= MAX_HEALTH) {
			this.setHealth(MAX_HEALTH);
		}
		this.setX(attackedCreature.getX());
		this.setY(attackedCreature.getY());
	}
	
	/**
	 * Special method that enables a Herbivore to find its prey with complete accuracy.
	 * Takes LocalInformation of the Herbivore and returns the valid creature to attack.
	 * @param localInformation the information of the Herbivore includes the information of its surroundings.
	 * @return Direction the direction of the suitable target to attack.
	 */
	public Direction findThePrey(LocalInformation localInformation) {
		List<Direction> directionList = new ArrayList<Direction>();
		if(localInformation.getCreatureDown() instanceof Plant) {
			directionList.add(Direction.DOWN);
		}
		if(localInformation.getCreatureLeft() instanceof Plant) {
			directionList.add(Direction.LEFT);
		}
		if(localInformation.getCreatureRight() instanceof Plant) {
			directionList.add(Direction.RIGHT);
		}
		if(localInformation.getCreatureUp() instanceof Plant) {
			directionList.add(Direction.UP);
		}
		if(directionList.size()==0) {
			return null;
		}
		Random rand = new Random();
		int index = rand.nextInt(directionList.size());
		return directionList.get(index);
	}

	/**
	 * specialized method of Herbivore that controls the motion of standing still.
	 * Loses life points less than moving, but gives no advantages in return.
	 * Neither useful nor harmful.
	 */
	@Override
	public void stay() {
		if(this.getHealth() <= 0.0) {
			this.setHealth(0.0);
			return;
		}
		this.setHealth(getHealth()-0.1);
	}

}
