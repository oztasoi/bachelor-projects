% ibrahim ozgurcan oztas
% 2016400198
% compiling: yes
% complete: yes

:-include('pokemon_data.pl').

% find_pokemon_evolution(+PokemonLevel, +Pokemon, -EvolvedPokemon)
find_pokemon_evolution(PokemonLevel, Pokemon, EvolvedPokemon):-
	pokemon_evolution(Pokemon, X, Y),
	Y=<PokemonLevel,
	find_pokemon_evolution(PokemonLevel,X,EvolvedPokemon).

find_pokemon_evolution(PokemonLevel, Pokemon, EvolvedPokemon):-
	EvolvedPokemon = Pokemon.

% pokemon_level_stats(+PokemonLevel, +Pokemon, -PokemonHp, -PokemonAttack, -PokemonDefense)
pokemon_level_stats(PokemonLevel, Pokemon, PokemonHp, PokemonAttack, PokemonDefense):-
	pokemon_stats(Pokemon, _, HealthPoint, AttackPoint, DefensePoint),
	PokemonHp is HealthPoint + 2 * PokemonLevel,
	PokemonAttack is AttackPoint + 1 * PokemonLevel,
	PokemonDefense is DefensePoint + 1 * PokemonLevel.

% single_type_multiplier(?AttackerType, ?DefenderType, ?Multiplier)
single_type_multiplier(AttackerType, DefenderType, Multiplier):-
	pokemon_types(TypeList),
	type_chart_attack(AttackerType,Hit_Ratio_List),
	nth1(Index, TypeList, DefenderType), %builtin array index predicate that I've used to find associated counterparts of variables when asked.
	nth1(Index, Hit_Ratio_List, Multiplier).

% type_multiplier(?AttackerType, ?DefenderTypeList, ?Multiplier)
type_multiplier(AttackerType, [Type1, Type2], Multiplier):-
	single_type_multiplier(AttackerType, Type1, Multiplier1),
	single_type_multiplier(AttackerType, Type2, Multiplier2),
	Multiplier is Multiplier1 * Multiplier2.

% pokemon_type_multiplier(?AttackerPokemon, ?DefenderPokemon, ?Multiplier)
% 4 case written separately.
pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier):-
	pokemon_stats(AttackerPokemon, Type_List_Attacker, _, _, _),
	pokemon_stats(DefenderPokemon, Type_List_Defender, _, _, _),
	length(Type_List_Attacker, Len1),
	length(Type_List_Defender, Len2),
	Len1 = 1, Len2 = 1, % Attacker has 1 type, Defender has 1 type.
	[Type_Attacker] = Type_List_Attacker,
	[Type_Defender] = Type_List_Defender,
	single_type_multiplier(Type_Attacker, Type_Defender, Multiplier).

pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier):-
	pokemon_stats(AttackerPokemon, Type_List_Attacker, _, _, _),
	pokemon_stats(DefenderPokemon, Type_List_Defender, _, _, _),
	length(Type_List_Attacker, Len1),
	length(Type_List_Defender, Len2),
	Len1 = 1, Len2 = 2, % Attacker has 1 type, Defender has 2 types.
	[Type_Attacker] = Type_List_Attacker,
	type_multiplier(Type_Attacker, Type_List_Defender, Multiplier).

pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier):-
	pokemon_stats(AttackerPokemon, Type_List_Attacker, _, _, _),
	pokemon_stats(DefenderPokemon, Type_List_Defender, _, _, _),
	length(Type_List_Attacker, Len1),
	length(Type_List_Defender, Len2),
	Len1 = 2, Len2 = 1, % Attacker has 2 types, Defender has 1 type.
	[Type_Attack_1, Type_Attack_2] = Type_List_Attacker,
	[Type_Defend] = Type_List_Defender,
	single_type_multiplier(Type_Attack_1, Type_Defend, Multiplier1),
	single_type_multiplier(Type_Attack_2, Type_Defend, Multiplier2),
	Multiplier is max(Multiplier1, Multiplier2).

pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier):-
	pokemon_stats(AttackerPokemon, Type_List_Attacker, _, _, _),
	pokemon_stats(DefenderPokemon, Type_List_Defender, _, _, _),
	length(Type_List_Attacker, Len1),
	length(Type_List_Defender, Len2),
	Len1 = 2, Len2 = 2, % Attacker has 2 types, Defender has 2 types.
	[Type_Attack_1, Type_Attack_2] = Type_List_Attacker,
	type_multiplier(Type_Attack_1, Type_List_Defender, Multiplier1),
	type_multiplier(Type_Attack_2, Type_List_Defender, Multiplier2),
	Multiplier is max(Multiplier1, Multiplier2).

% pokemon_attack(+AttackerPokemon, +AttackerPokemonLevel, +DefenderPokemon, +DefenderPokemonLevel, -Damage)
pokemon_attack(AttackerPokemon, AttackerPokemonLevel, DefenderPokemon, DefenderPokemonLevel, Damage):-
	pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, TypeMultiplier),
	pokemon_level_stats(AttackerPokemonLevel, AttackerPokemon, _, AttackerPokemonAttack, _),
	pokemon_level_stats(DefenderPokemonLevel, DefenderPokemon, _, _, DefenderPokemonDefense),
	Damage is (AttackerPokemonLevel * (AttackerPokemonAttack / DefenderPokemonDefense) * TypeMultiplier) / 2 + 1.

% pokemon_fight(+Pokemon1, +Pokemon1Level, +Pokemon2, +Pokemon2Level, -Pokemon1Hp, -Pokemon2Hp, -Rounds)
pokemon_fight(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level, Pokemon1AfterFightHp, Pokemon2AfterFightHp, TotalRound):-
	pokemon_attack(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level, Damage1),
	pokemon_attack(Pokemon2, Pokemon2Level, Pokemon1, Pokemon1Level, Damage2),
	pokemon_level_stats(Pokemon1Level, Pokemon1, Pokemon1Hp,_,_),
	pokemon_level_stats(Pokemon2Level, Pokemon2, Pokemon2Hp,_,_),
	pokemon_round_fight(Pokemon1Hp, Pokemon2Hp, Pokemon1AfterFightHp, Pokemon2AfterFightHp, Damage1, Damage2, TotalRound).

% For each round, both remaining HealthPoints are calculated, then recursively called the predicate.
pokemon_round_fight(Pokemon1Hp, Pokemon2Hp, Pokemon1EndFightHp, Pokemon2EndFightHp, Damage1, Damage2, TotalRound):-
	(Pokemon1Hp > 0, Pokemon2Hp > 0) ->
	Pokemon1RemainingHp is Pokemon1Hp - Damage2,
	Pokemon2RemainingHp is Pokemon2Hp - Damage1,
	pokemon_round_fight(Pokemon1RemainingHp, Pokemon2RemainingHp, Pokemon1EndFightHp, Pokemon2EndFightHp, Damage1, Damage2, CurrentRound),
	TotalRound is CurrentRound + 1;
	TotalRound is 0, Pokemon1EndFightHp is Pokemon1Hp, Pokemon2EndFightHp is Pokemon2Hp.

% pokemon_tournamet(+PokemonTrainer1, +PokemonTrainer2, -WinnerTrainer)	
pokemon_tournament(PokemonTrainer1, PokemonTrainer2, WinnerTrainerList):-
	pokemon_trainer(PokemonTrainer1, PokemonTrainer1PokemonList, PokemonTrainer1PokemonLevelList),
	pokemon_trainer(PokemonTrainer2, PokemonTrainer2PokemonList, PokemonTrainer2PokemonLevelList),
	pokemon_team_regulator(PokemonTrainer1PokemonList, PokemonTrainer1PokemonLevelList, PokemonTrainer1FinalPokemonList),
	pokemon_team_regulator(PokemonTrainer2PokemonList, PokemonTrainer2PokemonLevelList, PokemonTrainer2FinalPokemonList),
	pokemon_gotta_catch_em_all(PokemonTrainer1, PokemonTrainer1FinalPokemonList, PokemonTrainer1PokemonLevelList, PokemonTrainer2, PokemonTrainer2FinalPokemonList, PokemonTrainer2PokemonLevelList, WinnerTrainerList).

% regulator handles evolve part of the tournament for all pokemons
pokemon_team_regulator(PokemonTrainerPokemonList, PokemonTrainerPokemonLevelList, FinalPokemonList):-
	length(PokemonTrainerPokemonList, ListLength),
	ListLength > 0 ->
	PokemonTrainerPokemonList = [FirstPokemon | RemainingPokemonList],
	PokemonTrainerPokemonLevelList = [FirstPokemonLevel | RemainingPokemonLevelList],
	find_pokemon_evolution(FirstPokemonLevel, FirstPokemon, EvolvedPokemon),
	pokemon_team_regulator(RemainingPokemonList, RemainingPokemonLevelList, PokemonList),
	append([EvolvedPokemon], PokemonList, FinalPokemonList);
	append([],[],FinalPokemonList).

% gotta_catch_em_all handles pokemon fights 1 by 1, for each fight, outputs a winner. 3 cases are written separately.
% Pokemon1Hp greater than Pokemon2Hp
pokemon_gotta_catch_em_all(PokemonTrainer1, PokemonTrainer1PokemonList, PokemonTrainer1PokemonLevelList, PokemonTrainer2, PokemonTrainer2PokemonList, PokemonTrainer2PokemonLevelList, WinnerTrainerList):-
	length(PokemonTrainer1PokemonList, ListLength1),
	(ListLength1 > 0 ->
	PokemonTrainer1PokemonList = [FirstPokemon1 | RemainingPokemonList1],
	PokemonTrainer2PokemonList = [FirstPokemon2 | RemainingPokemonList2],
	PokemonTrainer1PokemonLevelList = [FirstPokemonLevel1 | RemainingPokemonLevelList1],
	PokemonTrainer2PokemonLevelList = [FirstPokemonLevel2 | RemainingPokemonLevelList2],
	pokemon_fight(FirstPokemon1, FirstPokemonLevel1, FirstPokemon2, FirstPokemonLevel2, Pokemon1AfterFightHp, Pokemon2AfterFightHp, _),
	Pokemon1AfterFightHp > Pokemon2AfterFightHp ->
	pokemon_gotta_catch_em_all(PokemonTrainer1, RemainingPokemonList1, RemainingPokemonLevelList1, PokemonTrainer2, RemainingPokemonList2, RemainingPokemonLevelList2, CurrentWinnerTrainerList),
	WinnerTrainerList = [PokemonTrainer1 | CurrentWinnerTrainerList];
	WinnerTrainerList = []).

% Pokemon1Hp lesser than Pokemon2Hp
pokemon_gotta_catch_em_all(PokemonTrainer1, PokemonTrainer1PokemonList, PokemonTrainer1PokemonLevelList, PokemonTrainer2, PokemonTrainer2PokemonList, PokemonTrainer2PokemonLevelList, WinnerTrainerList):-
	length(PokemonTrainer1PokemonList, ListLength1),
	(ListLength1 > 0 ->
	PokemonTrainer1PokemonList = [FirstPokemon1 | RemainingPokemonList1],
	PokemonTrainer2PokemonList = [FirstPokemon2 | RemainingPokemonList2],
	PokemonTrainer1PokemonLevelList = [FirstPokemonLevel1 | RemainingPokemonLevelList1],
	PokemonTrainer2PokemonLevelList = [FirstPokemonLevel2 | RemainingPokemonLevelList2],
	pokemon_fight(FirstPokemon1, FirstPokemonLevel1, FirstPokemon2, FirstPokemonLevel2, Pokemon1AfterFightHp, Pokemon2AfterFightHp, _),
	Pokemon1AfterFightHp < Pokemon2AfterFightHp ->
	pokemon_gotta_catch_em_all(PokemonTrainer1, RemainingPokemonList1, RemainingPokemonLevelList1, PokemonTrainer2, RemainingPokemonList2, RemainingPokemonLevelList2, CurrentWinnerTrainerList),
	WinnerTrainerList = [PokemonTrainer2 | CurrentWinnerTrainerList];
	WinnerTrainerList = []).

% Pokemon1Hp equals Pokemon2Hp
pokemon_gotta_catch_em_all(PokemonTrainer1, PokemonTrainer1PokemonList, PokemonTrainer1PokemonLevelList, PokemonTrainer2, PokemonTrainer2PokemonList, PokemonTrainer2PokemonLevelList, WinnerTrainerList):-
	length(PokemonTrainer1PokemonList, ListLength1),
	(ListLength1 > 0 ->
	PokemonTrainer1PokemonList = [FirstPokemon1 | RemainingPokemonList1],
	PokemonTrainer2PokemonList = [FirstPokemon2 | RemainingPokemonList2],
	PokemonTrainer1PokemonLevelList = [FirstPokemonLevel1 | RemainingPokemonLevelList1],
	PokemonTrainer2PokemonLevelList = [FirstPokemonLevel2 | RemainingPokemonLevelList2],
	pokemon_fight(FirstPokemon1, FirstPokemonLevel1, FirstPokemon2, FirstPokemonLevel2, Pokemon1AfterFightHp, Pokemon2AfterFightHp, _),
	Pokemon1AfterFightHp = Pokemon2AfterFightHp ->
	pokemon_gotta_catch_em_all(PokemonTrainer1, RemainingPokemonList1, RemainingPokemonLevelList1, PokemonTrainer2, RemainingPokemonList2, RemainingPokemonLevelList2, CurrentWinnerTrainerList),
	WinnerTrainerList = [PokemonTrainer1 | CurrentWinnerTrainerList];
	WinnerTrainerList = []).

% best_pokemon(+EnemyPokemon, +LevelCap, -RemainingHp, -BestPokemon)
best_pokemon(EnemyPokemon, LevelCap, RemainingHp, BestPokemon):-
	findall(Pokemon, pokemon_stats(Pokemon, _, _, _, _), SupremePokemon),
	pokemon_reign_supreme(EnemyPokemon, LevelCap, SupremePokemon, RemainingHp, BestPokemon).

% reign_supreme is the mindset to find the best pokemon against enemy pokemon.
pokemon_reign_supreme(EnemyPokemon, LevelCap, SupremePokemon, RemainingHp, BestPokemon):-
	SupremePokemon = [CurrentSupremePokemon | RemainingSupremePokemonList],
	(RemainingSupremePokemonList = [] ->
	BestPokemon = CurrentSupremePokemon,
	pokemon_fight(EnemyPokemon, LevelCap, CurrentSupremePokemon, LevelCap, _, CurrentSupremePokemonHp, _),
	RemainingHp is CurrentSupremePokemonHp;
	pokemon_fight(EnemyPokemon, LevelCap, CurrentSupremePokemon, LevelCap, _, CurrentSupremePokemonHp, _),
	pokemon_reign_supreme(EnemyPokemon, LevelCap, RemainingSupremePokemonList, RemainingSupremePokemonHp, RemainingBestPokemonCandidate),
	(CurrentSupremePokemonHp > RemainingSupremePokemonHp ->
	RemainingHp is CurrentSupremePokemonHp, BestPokemon = CurrentSupremePokemon;
	RemainingHp is RemainingSupremePokemonHp, BestPokemon = RemainingBestPokemonCandidate)).

% best_pokemon_team(+OpponentTrainer, -PokemonTeam)
best_pokemon_team(OpponentTrainer, PokemonTeam):-
	pokemon_trainer(OpponentTrainer, OpponentTrainerPokemonList, OpponentTrainerPokemonLevelList),
	pokemon_creed(OpponentTrainerPokemonList, OpponentTrainerPokemonLevelList, PokemonTeam).

% for each enemy pokemon, there exists a best counter pokemon at that levelcap. Creed unites all countering pokemon to 1 team.
pokemon_creed(OpponentTrainerPokemonList, OpponentTrainerPokemonLevelList, PokemonsCreed):-
	length(OpponentTrainerPokemonList, ListLength),
	(ListLength > 0 ->
	OpponentTrainerPokemonList = [CurrentPokemon | RemainingPokemonList],
	OpponentTrainerPokemonLevelList = [CurrentPokemonLevel | RemainingPokemonLevelList],	
	find_pokemon_evolution(CurrentPokemonLevel, CurrentPokemon, EvolvedPokemon),
	best_pokemon(EvolvedPokemon, CurrentPokemonLevel, _, EvolvedSupremePokemon),
	pokemon_creed(RemainingPokemonList, RemainingPokemonLevelList, RemainingPokemonsCreed),
	append([EvolvedSupremePokemon], RemainingPokemonsCreed, PokemonsCreed);
	append([], [], PokemonsCreed)).

% pokemon_types(+TypeList, +InitialPokemonList, -PokemonList)
pokemon_types(TypeList, InitialPokemonList, PokemonList):-
	findall(Pokemon, (member(Pokemon, InitialPokemonList), pokemon_type_check(TypeList, Pokemon)), PokemonList).

% In Problem Session, this predicate is written and I've used it.
pokemon_type_check(Typelist, Pokemon):-
	Typelist = [FirstType | RemainingTypeList],
	pokemon_stats(Pokemon, PokemonTypeList, _, _, _),
	((member(FirstType, PokemonTypeList), !); pokemon_type_check(RemainingTypeList, Pokemon)).

% generate_pokemon_team, I've separated it 3 part, for each character and evaluate it thoroughly, but some mistakes may occur.
% the test predicate in description is somewhat behaving oddly.
% generate_pokemon_team(+LikedTypes, +DislikedTypes, +Criterion, +Count, -PokemonTeam)
	
generate_pokemon_team(LikedTypes, DislikedTypes, 'a', Count, PokemonList):-
	findall(Pokemon, (pokemon_stats(Pokemon, _, _, _, _)), PokemonUniteList),
	pokemon_types(LikedTypes, PokemonUniteList, LikedPokemonList),
	pokemon_types(DislikedTypes, LikedPokemonList, ImprovedPokemonList),
	subtract(LikedPokemonList, ImprovedPokemonList, PokemonTeam),
	findall(PokemonAttack, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, _, PokemonAttack, _)), PokemonAttackList),
	sort(0, @>=, PokemonAttackList, SortedAttackList),
	pokemon_list_divider_attack(SortedAttackList, PokemonTeam, Count, PokemonNameList),
	print_list(PokemonNameList, PokemonList).

generate_pokemon_team(LikedTypes, DislikedTypes, 'd', Count, PokemonList):-
	findall(Pokemon, (pokemon_stats(Pokemon, _, _, _, _)), PokemonUniteList),
	pokemon_types(LikedTypes, PokemonUniteList, LikedPokemonList),
	pokemon_types(DislikedTypes, LikedPokemonList, ImprovedPokemonList),
	subtract(LikedPokemonList, ImprovedPokemonList, PokemonTeam),
	findall(PokemonDefense, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, _, _, PokemonDefense)), PokemonDefenseList),
	sort(0, @>=, PokemonDefenseList, SortedDefenseList),
	pokemon_list_divider_defense(SortedDefenseList, PokemonTeam, Count, PokemonNameList),
	print_list(PokemonNameList, PokemonList).

generate_pokemon_team(LikedTypes, DislikedTypes, 'h', Count, PokemonList):-
	findall(Pokemon, (pokemon_stats(Pokemon, _, _, _, _)), PokemonUniteList),
	pokemon_types(LikedTypes, PokemonUniteList, LikedPokemonList),
	pokemon_types(DislikedTypes, LikedPokemonList, ImprovedPokemonList),
	subtract(LikedPokemonList, ImprovedPokemonList, PokemonTeam),
	findall(PokemonHealth, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, PokemonHealth, _, _)), PokemonHealthList),
	sort(0, @>=, PokemonHealthList, SortedHealthList),
	pokemon_list_divider_health(SortedHealthList, PokemonTeam, Count, PokemonNameList),
	print_list(PokemonNameList, PokemonList).

print_list([],[]).
print_list([First|Last], [Final|Rest]):-
	pokemon_stats(First, _, B, _, _),
	pokemon_stats(First, _, _, C, _),
	pokemon_stats(First, _, _, _, D),
	Final = [First, B, C, D],
	print_list(Last, Rest).

pokemon_list_divider_attack([First | RestList], PokemonTeam, Count, ReturnList):-
	findall(Pokemon, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, _, First, _)), TempList),
	length(TempList, ListLength),
	(Count > 0 ->
		(Count > ListLength ->
			CurrentCount is Count - ListLength,
			(member(First, RestList) ->
				subtract(RestList, [First], AttackResultList);
				AttackResultList = RestList),
			pokemon_list_divider_attack(AttackResultList, PokemonTeam, CurrentCount, TempReturnList),
			append(TempList, TempReturnList, ReturnList);
			pokemon_list_divider_attack(AttackResultList, PokemonTeam, 0, TempReturnList),
			CountCount is ListLength - Count,
			trim(TempList, CountCount, ResultList),
			append(ResultList, TempReturnList, ReturnList));
		append([], [], ReturnList)).

pokemon_list_divider_defense([First | RestList], PokemonTeam, Count, ReturnList):-
	findall(Pokemon, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, _, _, First)), TempList),
	length(TempList, ListLength),
	(Count > 0 ->
		(Count > ListLength ->
			CurrentCount is Count - ListLength,
			(member(First, RestList) ->
				subtract(RestList, [First], DefenseResultList);
				DefenseResultList = RestList),
			pokemon_list_divider_defense(DefenseResultList, PokemonTeam, CurrentCount, TempReturnList),
			append(TempList, TempReturnList, ReturnList);
			pokemon_list_divider_defense(DefenseResultList, PokemonTeam, 0, TempReturnList),
			CountCount is ListLength - Count,
			trim(TempList, CountCount, ResultList),
			append(ResultList, TempReturnList, ReturnList));
		append([], [], ReturnList)).

pokemon_list_divider_health([First | RestList], PokemonTeam, Count, ReturnList):-
	findall(Pokemon, (member(Pokemon, PokemonTeam), pokemon_stats(Pokemon, _, First, _, _)), TempList),
	length(TempList, ListLength),
	(Count > 0 ->
		(Count > ListLength ->
			CurrentCount is Count - ListLength,
			(member(First, RestList) ->
				subtract(RestList, [First], HealthResultList);
				HealthResultList = RestList),
			pokemon_list_divider_health(HealthResultList, PokemonTeam, CurrentCount, TempReturnList),
			append(TempList, TempReturnList, ReturnList);
			pokemon_list_divider_health(HealthResultList, PokemonTeam, 0, TempReturnList),
			CountCount is ListLength - Count,
			trim(TempList, CountCount, ResultList),
			append(ResultList, TempReturnList, ReturnList));
		append([], [], ReturnList)).

% I've searched through internet and find how to trim N elements of a list via prolog.
% The link is "https://stackoverflow.com/questions/27479915/how-to-trim-first-n-elements-from-in-list-in-prolog"
trim(List,Count,ResultList) :-    
  length(P,Count), append(P,ResultList,List).