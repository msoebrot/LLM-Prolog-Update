% Last Update Time: 12:00:00 April 1 2024

% Facts
student(michael, [2024, 04, 01]).
outdoor(pool, [2024, 01, 01]).
openingHours(pool, monday, 0900, 1900, [2024, 04, 01]).
quarter(winter, 01, 03, [2024, 04, 01]).
prefer_cuisine(priyesh, thai, [2024, 04, 01]).
prefer_cuisine(priyesh, chinese, [2024, 03, 01]).
cuisineAt(monday, lunch, thai, stevenson, [2024, 03, 23]).
cuisineAt(monday, lunch, chinese, cowell, [2024, 03, 13]).
number_of_dining_halls(5, [2024, 04, 01]).
dining_hall(stevenson, [2024, 03, 01]).
dining_hall(cowell, [2024, 03, 01]).
dining_hall(crown_merrill, [2024, 03, 01]).
dining_hall(colleges_nine_ten, [2024, 04, 01]).
dining_hall(porter_kresge, [2024, 02, 01]).
dining_hall(rachel_carson_oakes, [2024, 02, 01]).

% Rules

not(P) :- P, !, fail ; true.

study_place(X, [quiet, wifi], [Year, Month, Date]) :- student(X, [Year, Month, Date]).
study_place(X, [home], [Year, Month, Date]) :- not(student(X, [Year, Month, Date])).

status(X, Hour, Day, [p_weather], [Year, Month, Date]) :- isOpen(X, Hour, Day), outdoor(X, [Year, Month, Date]).
isOpen(X, Hour, Day, [Year, Month, Date]) :- openingHours(X, Day, Opening, Closing, [Year, Month, Date]), Hour > Opening, Hour < Closing.

meal(Hour, lunch) :- Hour > 1200, Hour < 1500.
dineAt(Name, Hour, Day, DiningHall, Cuisine, [Year, Month, Date]) :- prefer_cuisine(Name, Cuisine, [Year, Month, Date]), meal(Hour, Type), cuisineAt(Day, Type, Cuisine, DiningHall, [_, _, _]).

drop_classes(_, Month, ['29', 'jan'], [Year, Month, Date]) :- quarter(winter, Start, End, [Year, Month, Date]), Month >= Start, Month =< End.