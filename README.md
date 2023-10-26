
# Recipe Management System

# Funkcje

- baza przepisów (create, edit, delete)
- baza zarejestrowanych użytkowników (not registered == read only)
- filtrowanie/sortowanie po składnikach/czasie/kategorii
- (?) input ingredients -> get a recipe
- admin -> CRUD on users

# Bazy danych

- recipes (name, author, time, ingredients, difficulty level, instructions, type, *rating*)
  - ingredients (name, quantity/unit of measurement)
- users/authors (name, username, bio, *public/private if you don't want to share your secrets*)

# Wymagania

- 4-5 modeli
  - dodać komentarze?/posty lifestyle poza przepisami/komunikacja między autorami
- uwierzytelnianie i autoryzacja
- endpointy dla: CRUD i coś co nie jest CRUDem
