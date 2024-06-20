//Alumnos: Alberto Olcina Calabuig y Alma Salmerón Sena

+flag(F): team(200)
  <-
  ?position(G);
  .getNearestCentralLimit(G, P);
  .goto(P).

+health(H): H < 30
  <-
  -giro;
  +center;
  .goto([128, 0, 128]).

+ammo(A): A < 30
  <-
  -giro;
  +center;
  .goto([128, 0, 128]).

+health(H): H > 75 & center & ammo(A) & A > 75
  <-
  -center;
  ?position(G);
  .getNearestCentralLimit(G, P);
  .goto(P).

+ammo(H): H > 75 & center & health(A) & A > 75
  <-
  -center;
  ?position(G);
  .getNearestCentralLimit(G, P);
  .goto(P).

+packs_in_fov(ID, Type, Angle, Distance, Health, Position) : not(gettingPack) & ammo(A) & A < 75 & Type == 1002
  <-
  +gettingPack;
  .goto(Position).

+packs_in_fov(ID, Type, Angle, Distance, Health, Position) : not(gettingPack) & health(H) & H < 100 & Type == 1001
  <-
  +gettingPack;
  .goto(Position).


+pack_taken(N, T): team(200)
  <-
  -gettingPack.


+target_reached(T): not(center) & team(200)
  <-
  .getInitialLookAt(T, L);
  .look_at(L);
  +giro;
  +turnAroundA(0);
  -target_reached(T).

+turnAroundA(B) : giro & not(enemiesDetected)
  <-
  ?position(P);
  .wait(500);
  .lookSideOne(P,M);
  .look_at(M);
  .wait(100);
  +turnAroundB(0);
  -turnAroundA(B).

+turnAroundB(C) : giro & not(enemiesDetected)
  <-
  ?position(P);
  .wait(500);
  .getInitialLookAt(P, N);
  .look_at(N);
  .wait(100);
  +turnAroundC(0);
  -turnAroundB(C).

  +turnAroundC(D) : giro & not(enemiesDetected)
  <-
  ?position(P);
  .wait(500);
  .lookSideTwo(P, Q);
  .look_at(Q);
  .wait(100);
  +turnAroundA(0);
  -turnAroundC(D).

+patroll_point(P): total_control_points(T) & P<T
  <-
  ?control_points(C);
  .nth(P,C,A);
  .goto(A).
 // .print("Voy a Pos: ", A).

+patroll_point(P): total_control_points(T) & P==T
  <-
  -patroll_point(P);
  +patroll_point(0).
 
 /*  En modo arena no hace falta disparar al enemigo  
  +enemies_in_fov(ID,Type,Angle,Distance,Health,Position) :  health(H) & H > 75 & ammo(A) & A > 35
  <-
  +enemiesDetected;
  .shoot(20,Position);
  -enemiesDetected;
*/
  
+friends_in_fov(ID,Type,Angle,Distance,Health,Position) : ammo(A) & A > 0 & health(H) & H > 30
  <-
  +enemiesDetected;
  .shoot(20,Position);
  +noEnemies(0).

+noEnemies(E) : enemiesDetected
  <-
  .wait(400);
  -enemiesDetected.
