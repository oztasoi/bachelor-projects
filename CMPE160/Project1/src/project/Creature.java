package project;

import naturesimulator.Action;
import naturesimulator.LocalInformation;
import game.Drawable;
import game.Direction;

/**
 * General Class that has been used to configure the basic entire specs of the simulator.
 * The one sole ancestor of other classes.
 * @author Ozgurcan Oztas
 *
 */
public abstract class Creature implements Drawable {

	
		/**
		 * x field is the x value of the coordinate of the creature which is created.
		 */
		private int x;
		
		/**
		 * y field is the y value of the coordinate of the creature which is created.
		 */
		private int y;
		
		/**
		 * health field is the health value of the creature that corresponds to its life points. 
		 */
		private double health;
		
		
		/**
		 * getter method of the x field of class Creature
		 * @return x returns x value of the coordinate of the creature.
		 */
		public int getX() {
			return x;
		}

		
		/**
		 * getter method of the y field of the class Creature
		 * @return y returns y value of the coordinate of the creature.
		 */
		public int getY() {
			return y;
		}
		
		
		/**
		 * getter method of the health field of the class Creature
		 * @return health returns the life point of the creature.
		 */
		public double getHealth() {
			return health;
		}

		
		/**
		 * setter method of the x field to the parameter _x of the class Creature
		 * @param _x sets the x component of the coordinate of the creature.
		 */
		public void setX(int _x) {
			this.x = _x;
		}

		/**
		 * setter method of the y field to the parameter _y of the class Creature
		 * @param _y sets the y component of the coordinate of the creature.
		 */
		public void setY(int _y) {
			this.y = _y;
		}
		
		
		/**
		 * setter method of the health field to the parameter _health of the class Creature
		 * @param _health the numerical value of the life point of creature.
		 */
		public void setHealth(double _health) {
			this.health = _health;
		}

		
		/**
		 * general constructor of the class Creature with the given parameters.
		 * @param _x the x component of the coordinate
		 * @param _y the y component of the coordinate
		 */
		public Creature(int _x, int _y) {
			this.x = _x;
			this.y = _y;
		}
		
		/**
		 * general conception of the Creature that takes LocalInformation as a parameter and returns a valid action.
		 * @param localInformation the information of a Creature includes the information of surroundings of it.
		 * @return new Action(Type.type), new Action(Type.type, Direction direction)
		 */
		public abstract Action chooseAction(LocalInformation localInformation);
		
		
		/**
		 * general reproduction method of the Creature that takes LocalInformation as a parameter and returns a new Creature.
		 * @param direction a suitable direction which is decided by the  @method chooseAction. 
		 * @return new Creature(Integer _x, Integer _y, double _health);
		 */
		public abstract Creature reproduce(Direction direction);
		
		
		/**
		 * general attack method of the suitable Creature that takes Creature as a valid attacking target and siphons its complete health.
		 * Therefore, target's health will be equalized to zero.
		 * @param attackedCreature a suitable target to attack.
		 */
		public void attack(Creature attackedCreature) {
			
		}
		
		
		/**
		 * general movement method of the suitable Creature that takes Direction as a valid direction to move and moves there.
		 * @param direction a suitable direction to move.
		 */
		public void move(Direction direction) {
			if(direction == Direction.DOWN) {
				this.y++;
			}
			else if(direction == Direction.UP) {
				this.y--;
			}
			else if(direction == Direction.LEFT) {
				this.x--;
			}
			else {
				this.x++;
			}
			this.setHealth(getHealth()-1.0);
			
		}
		
		
		/**
		 * general standing method of the Creature that either does photosynthesis to increase its health or stands still to spend less life point than moving. 
		 */
		public abstract void stay();
}
