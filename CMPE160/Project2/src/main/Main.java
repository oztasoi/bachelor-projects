package main;

import java.awt.EventQueue;

import environment.SnakeWars;
import ui.ApplicationWindow;

/**
 * The main class of the project.
 * 
 * @author Ozgurcan Oztas
 */
public class Main {

	/**
	 * Main entry point for the application.
	 *
	 * @param args
	 *            application arguments
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(() -> {
			SnakeWars game = new SnakeWars(25, 25, 30, 100);
			
			// Create application window that contains the game panel
			ApplicationWindow window = new ApplicationWindow(game.getGamePanel());
			window.getFrame().setVisible(true);
			
			game.start();
		});
	}
}
