package environment;

import game.Direction;


/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class Action {

    /**
     * Enum representing possible action types
     */
    public enum Type {
        MOVE,
        REPRODUCE,
        EAT,
        STAY,
    }

    private final Type type;
    private final Direction direction;

    /**
     * Creates an action without direction
     * @throws IllegalArgumentException in case the action type requires a direction
     * @param type action type
     */
    public Action(Type type) {
        if (type == Type.MOVE) {
            throw new IllegalArgumentException("You cannot create an action "
                    + "of type " + type + " without a direction");
        }
        this.type = type;
        direction = null;
    }

    /**
     * Creates an action with direction
     * @throws IllegalArgumentException in case the action type must not have a direction
     * @param type action type
     * @param direction direction
     */
    public Action(Type type, Direction direction) {
        if (type == Type.STAY || type == Type.REPRODUCE || type == Type.EAT) {
            throw new IllegalArgumentException("Action of type "
                    + type + " should be created without a direction");
        }
        this.type = type;
        this.direction = direction;
    }

    /**
     * Getter for the type of the action
     * @return action type
     */
    public Type getType() {
        return type;
    }

    /**
     * Getter for the direction of the action
     * @return direction or null if a direction does not exist
     */
    public Direction getDirection() {
        return direction;
    }

}
