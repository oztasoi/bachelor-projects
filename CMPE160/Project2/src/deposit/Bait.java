package deposit;

import java.awt.Color;

import game.Drawable;
import ui.GridPanel;
/**
 * 
 * @author Ozgurcan Oztas
 *
 */
public class Bait extends Node implements Drawable {

	/**
	 * 
	 * @param coordinate takes coordinate as a component of x and y couple.
	 */
	public Bait(Coordinate coordinate) {
		super(coordinate);
	}
	
	@Override
	public void draw(GridPanel panel) {
		panel.drawSquare(x, y, Color.YELLOW);
		
	}

	
}
