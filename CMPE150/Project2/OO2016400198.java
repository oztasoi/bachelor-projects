import java.util.*;
public class OO2016400198 {

	
	public static void main(String[] args) {
		Scanner console = new Scanner(System.in);
		//This is the introduction part of my code. There is a smooth and funny entrance part by requesting from user to type 1 and press enter.
		//Then firstStep method initializes.
		intro(console);
		//this method is created to gather user's name and age to proceed further steps. Evaluation of the user's age is important,
		//because the restrictions implies that user should be equal or more than 18 years old.
		firstStep(console);
		//this method is created to gather the information of user's sex to determine whether or not user is male.
		//If the user is male, the method requires whether or not user has completed his military service.
		secondStep(console);
		//this method is the core part of my program, because it requires the name of the job which the user applies for.
		//and it has submethods that helps this method to evaluate the user.
		thirdStep(console);
	}
	public static void intro(Scanner console){
		System.out.println("Welcome to the MARS Enterprises.");			
		System.out.println("For the security of both of the sides, your informations are secured with MARS Security.");			
		System.out.println("This program was designed to elect among individuals \nwho may become the possible employee of our company. ");
		System.out.println("If you are ready, confirm that you are no robot by typing 1 and pressing enter.");			
		//commence is the string variable I request from user to determine whether or not the user is human. 
		String commence = console.nextLine();
		if (commence.equals("1")){
			System.out.println("Status: You are allowed to proceed.");			
		}
		else{
			System.out.println("ERROR: Inorganic invasion. Immediate termination NOW!!!!");
			System.exit(1);
		}
	}
	public static void firstStep(Scanner console){
		
		System.out.println("To avoid a boring worklife and working environment,\nMARS Enterprises is looking for some funny people with amazing background.\nAre you worthy to become the next generation of JOKE?");
		System.out.println("Let's begin with the first question. What's the word which the people call y0u?");
		String name = console.nextLine();
		System.out.println("Hello " + name + ".");
		if(name.toUpperCase().charAt(0) == 'M'){
				System.out.println("What a nice name. \nYou have a head start from the beginning. Very Nice! :')");
		} 
		else {
				System.out.println("Your parents should name you with a name starting with M. \nWhat a shame! :'(");
		}
		System.out.println("Now, let's learn your age. \nHow many year passed since you were extracted from your mother's belly?");
		int age = console.nextInt();
		if (age >= 18){
				System.out.println("You have lived long enough without us. \nNow live with us if you are worthy.");
				System.out.println("First step is completed. \nProceeding with second step now.");
		}
		else{
				System.out.println("Your mother had a big mistake when she gave birth to you at a late time. \nShe should have done it way before.");
				System.out.println("Sorry, but you are not old enough to make a difference in our company. \nCome later again. ");
				System.exit(1);
		}
	}
	public static void secondStep(Scanner console){
		
		System.out.println("Here we are at the second step. That's an easy one, I guarantee you.");
		System.out.println("Tell me you sex: Male or Female?");
		//sex is the string variable I request from user to determine the sex to generate input for the next logical evaluation which is whether the user is man or woman.
		String sex = console.next();
		if (sex.toLowerCase().equals("male")){
			
			System.out.println("Wow. You are a man, I see. But are you a real man? \nHave you completed your military service? Type \"yes\" or \"no\".");
			String militaryService = console.next();
			if(militaryService.toLowerCase().equals("yes")){
				
				System.out.println("You're amazing maaan. I knew you are one of those superpowered patriots. Yehhhuu!");
				System.out.println("Okay then. Let's continue with the basis of this auto-interviewing program. The position...");
			}
			else if (militaryService.toLowerCase().equals("no")){
				System.out.println("What a shame! Before I report you to the military garnison in this city, get out of our company, NOW YOU COWARD!!!");
				System.exit(1);
			}
			else{
				System.out.println("Unknown command: Shutdown initiated.");
				System.exit(1);
			}
		}
		else if(sex.toLowerCase().equals("female")){
			System.out.println("I see, you are very well-looking female. You may become our face model maybe, what do you say?");
			System.out.println("I think you should continue. :')");
		}
		else{
			System.out.println("Undefined type of sex. Possible invasion of machines. Termination engaged.");
			System.exit(1);
		}
	}
	public static void thirdStep(Scanner console){
		
		System.out.println("Here we are, at the gate of your career. Tell me my possible fellow employee,");
		System.out.println("Which department are you making an application?");
		System.out.println("Type the number of the job you're applying for. ");
		System.out.println("1 - Software Engineer");
		System.out.println("2 - Accountant");
		System.out.println("3 - Academic");
		console.nextLine();
		String position = console.nextLine();
		
		if(position.equals("1")){
			softwareEngineer(console);
		}
		else if(position.equals("2")){
			accountant(console);
		}
		else if(position.equals("3")){
			academic(console);
		}
		else {
			System.out.println("Undefined position. Program is closed.");
			System.exit(1);
		}
	}
	//this method decides the user has all the requirements of the company's traits. By taking variables at multiple types,
	//this method makes an assessment about the user and determines whether the user is worthy for the position or not.
	public static void softwareEngineer(Scanner console){
		System.out.println("Now, tell me. What was the major in your university?");
		System.out.println("To get the job, you should have studied one of these majors written below.");
		System.out.println("Type the number of the major you've studied: ");
		System.out.println("1- Software Engineering");
		System.out.println("2- Computer Engineering");
		System.out.println("3- Computer Sciences");
		String major = console.nextLine();
		if(major.equalsIgnoreCase("1")){
			if(pcLang(console)>=2){
				System.out.println("Great. You have some skills I see.");
				System.out.println("But, do you have work experience ?");
				System.out.println("How many years did you worked before applying our corporation as a software engineer?");
				int year = console.nextInt();
				System.out.println("Let me ask you another question. Do you have a graduate degree on software engineering? Type \"yes\" or \"no\".");
				console.nextLine();
				String answer = console.nextLine();
				if(year>=3 || answer.equalsIgnoreCase("yes")){
					System.out.println("You are a very qualified indiviual I see. With this background, you should be able to work in our company.");
					System.out.println(finalAnswer(console));
				}
				else{
					System.out.println("Sorry, but we've expected higher traits of you. Maybe next time...");
					System.exit(1);
				}
			}
			else{
				System.out.println("Communication is the deal, but communication with computers is the real deal.");
				System.exit(1);
			}
			
		}
		else if (major.equalsIgnoreCase("2")){
			if(pcLang(console)>=2){
				System.out.println("Great. You have some skills I see.");
				System.out.println("But, do you have work experience ?");
				System.out.println("How many years did you worked before applying our corporation as a software engineer?");
				int year = console.nextInt();
				System.out.println("Let me ask you another question. Do you have a graduate degree on software engineering? Type \"yes\" or \"no\".");
				console.nextLine();
				String answer = console.nextLine();
				if(year>=3 || answer.equalsIgnoreCase("yes")){
					System.out.println("You are a very qualified indiviual I see. With this background, you should be able to work in our company.");
					System.out.println(finalAnswer(console));
				}
				else{
					System.out.println("Sorry, but we've expected higher traits of you. Maybe next time...");
					System.exit(1);
				}
			}
			else{
				System.out.println("Communication is the deal, but communication with computers is the real deal.");
				System.exit(1);
			}
		}
		else if (major.equalsIgnoreCase("3")){
			if(pcLang(console)>=2){
				System.out.println("Great. You have some skills I see.");
				System.out.println("But, do you have work experience ?");
				System.out.println("How many years did you worked before applying our corporation as a software engineer?");
				int year = console.nextInt();
				System.out.println("Let me ask you another question. Do you have a graduate degree on software engineering? Type \"yes\" or \"no\".");
				console.nextLine();
				String answer = console.nextLine();
				if(year>=3 || answer.equalsIgnoreCase("yes")){
					System.out.println("You are a very qualified indiviual I see. With this background, you should be able to work in our company.");
					System.out.println(finalAnswer(console));
				}
				else{
					System.out.println("Sorry, but we've expected higher traits of you. Maybe next time...");
					System.exit(1);
				}
			}
			else{
				System.out.println("Communication is the deal, but communication with computers is the real deal.");
				System.exit(1);
			}
		}
		else {
			System.out.println("Unknown type : Shutdown initiated.");
			System.exit(1);
		}
	}
	//this method decides the user has all the requirements of the company's traits. By taking variables at multiple types,
	//this method makes an assessment about the user and determines whether the user is worthy for the position or not.
	public static void accountant(Scanner console){
		System.out.println("Do you have an accounting degree? Type \"yes\" or \"no\". ");
		String answer = console.next();
		if(answer.equals("yes")){
			System.out.println("Great. Then, do you know how to use Excel very well? Type \"yes\" or \"no\".");
			String answer2 = console.next();
			if(answer2.equals("yes")){
				System.out.println("Wonderful. By the way let me ask you another questions.");
				System.out.println("First question is do you speak English fluently?");
				System.out.println("And the second is do you have friends who can translate English for you?");
				System.out.println("Type \"yes\" or \"no\" for both.");
				String answer3 = console.next();
				String answer4 = console.next();
				if (answer3.equals("yes") || answer4.equals("yes")){
					System.out.println("How many people do you know in MARS Enterprises? ");
					int num = console.nextInt();
					if(num >=2 ){
						System.out.println("Final question : Do you have a driving license? That's very important that you have one.");
						System.out.println("Type \"yes\" or \"no\". Last question btw. You can do it! :')");
						String finanswer = console.next();
						if(finanswer.equals("yes")){
							System.out.println("OH MY GOD! The person we are looking for is you. You will be one of us if you choose to accept our conditions.");
							System.out.println("Thanks for so much effort and time. Waiting your final answer. :D");
							System.out.println(finalAnswer(console));
						}
						else{
							System.out.println("Ah. You were so close to get this job, but not enough I see. Before next time, learn where the handbrake is.");
							System.exit(1);
						}
					}
					else if(num<2 && 0<num){
						System.out.println("Sorry but your business network inside our organization is too small. Until next time try to make new friends, okay?");
						System.exit(1);
					}
					else{
						System.out.println("Illogical situation. Termination is begun.");
						System.exit(1);
					}
				}
				else{
					System.out.println("Dude what's the meaning of that. Are you saying that you can't even speak to someone who knows English?");
					System.out.println("That's unacceptable. Can you even understand what I am saying? ");
					System.out.println("Let me give you the address of our Language Education Center. Good luck until next time! ");
					System.exit(1);
				}
			}
			else{
				System.out.println("Hmm. Let me arrange you some personal improvement class at Boðaziçi University Computer Engineering.");
				System.out.println("I'm sure they are way too experienced that you need but they'll help you to learn some Excel.");
				System.out.println("Maybe you can learn it on your own. Your choice at the end. Goodbye!");
				System.exit(1);
			}
		}
		else{
			System.out.println("Why did you even apply for this job without a accounting major? Go to a university to save yourself from your ignorance.");
			System.exit(1);
		}
	}
	//this method decides the user has all the requirements of the company's traits. By taking variables at multiple types,
	//this method makes an assessment about the user and determines whether the user is worthy for the position or not.
	public static void academic(Scanner console){
		
		System.out.println("You want to be our academic. Okay then. Can you speak English?");
		System.out.println("Type \"yes\" or \"no\".");
		String answer = console.next();
		if(answer.equals("yes")){
			System.out.println("How many papers have you published since the beginning your academic career?");
			int num = console.nextInt();
			if(num >=3){
				System.out.println("Excellent work. Final question is at hand.");
				System.out.println("Do you love to teach? Type \"yes\" or \"no\".");
				String answer2 = console.next();
				if(answer2.equals("yes")){
					String output = finalAnswer(console);
					System.out.println(output);
					
				}
				else {
					System.out.println("An academic who was raised by and academic should at least love his/her job. Sorry but you can't sit with us.");
					System.exit(1);
				}
			}
			else if (0<num && num<3){
				System.out.println("You should have published more papers. I assume you haven't learned the complete of your major. Work harder!!! See ya :')");
				System.exit(1);
			}
			else {
				System.out.println("Have you ever publish a paper? I am just curious. However, this conversation is over.");
				System.exit(1);
			}
		}
		else {
			System.out.println("In our world, everything uses English to communicate with each other.\nYou may not understand what I'm saying, but basicly, \"NOT ENGLÝSH,JUST ENGLISH\"");
			System.exit(1);
		}
	}
	//this method decides whether the user knows equal or more than 2 languages or not. It takes data from scanner and
	//return the number of the languages which user knows.
	public static int pcLang(Scanner console){
		int count = 0;
		System.out.println("Now, let me ask you some questions.");
		System.out.println("Do you know how to program in Java? Type \"yes\" or \"no\".");
		String answer = console.nextLine();
		if(answer.equalsIgnoreCase("yes")){
			count++;
		}
		else if(answer.equalsIgnoreCase("no")){
			System.out.println("Java is not just the coffee, mate. Learn some.");
		}
		else{
			System.out.println("Wrong input. Shutdown initiated.");
			System.exit(1);
		}
		System.out.println("Do you know how to program in C? Type \"yes\" or \"no\".");
		String answer2 = console.nextLine();
		if(answer2.equalsIgnoreCase("yes")){
			count++;
		}
		else if(answer2.equalsIgnoreCase("no")){
			System.out.println(":'(");
		}
		else{
			System.out.println("Wrong input. Shutdown initiated.");
			System.exit(1);
		}
		System.out.println("Do you know how to program in Prologue? Type \"yes\" or \"no\".");
		String answer3 = console.nextLine();
		if(answer3.equalsIgnoreCase("yes")){
			count++;
		}
		else if(answer3.equalsIgnoreCase("no")){
			System.out.println("What a pity.");
		}
		else{
			System.out.println("Wrong input. Shutdown initiated.");
			System.exit(1);
		}
		return count;
	}
	//this is the optional method I've created to reduce the monotonous aura of the program.
	public static String finalAnswer(Scanner console){
		System.out.println("There is no problem for hiring you. But do you want to be a part of us?");
		System.out.println("Type \"yes\" or \"no\".");
		String FinalAnswer = console.next();
		if(FinalAnswer.equals("yes")){
			return "You have passed all the questions. By the rules of MARS Enterprises, I hereby commission you under MARS Enterprises.\nWelcome to outer space, my fellow colleague! Live the way you live!!!";
		
		}
		else {
			return "I wish I could change your mind. But, maybe that's how it should be after all. Be careful and successful at your life. Thanks for your interest. Bye Bye !!!";
		}
	}
}

