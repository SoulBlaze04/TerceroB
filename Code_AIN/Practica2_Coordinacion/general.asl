// TEAM_ALLIED

+flag(F): team(100) & not(initial)
  <-
  .register_service("allied");
  .print("Inicio general");
  .register_service("general");
  .wait(4000);
  .get_service("comandante");
  .get_medics;
  .get_fieldops;
  .get_service("soldier");
  .wait(5000);
  +notPosition;
  +initial;
  !!crear_formacion.

+estoy_en_posicion[source(A)] : team(100) & contador(C) & C < 8
  <-
  .print(C);
  -+contador(C + 1).

+estoy_en_posicion[source(A)] : team(100) & contador(C) & C > 7
  <-
  ?unifiedList(L);
  -contador(_);
  .send(L, tell, reachingFinalPoint).
  


+!crear_formacion: team(100) & notPosition
  <-
  ?flag(F);
  ?comandante(C);
  ?myMedics(M);
  ?myFieldops(R);
  ?soldier(S);
  .send(S, tell, mando_medicos(M));
  .send(S, tell, mando_recargas(R));
  .print(C);
  .print(M);
  .print(R);
  .print(S);
  .unifiedList(C,M,R,S,L);
  +unifiedList(L);
  .print(L);
  ?base(B);
  .print(B);
  ?flag(V);
  .print(V);
  .startingPositions(B,F,P);
  +contador(0);
  .nth(0,L,L0);
  .nth(1,L,L1);
  .nth(2,L,L2);
  .nth(3,L,L3);
  .nth(4,L,L4);
  .nth(5,L,L5);
  .nth(6,L,L6);
  .nth(7,L,L7);
  .nth(8,L,L8);
  .print(P);
  .nth(0,P,P0);
  .nth(1,P,P1);
  .nth(2,P,P2);
  .nth(3,P,P3);
  .nth(4,P,P4);
  .nth(5,P,P5);
  .nth(6,P,P6);
  .nth(7,P,P7);
  .nth(8,P,P8);
  .send(L0, tell, initPos(P0));
  .send(L1, tell, initPos(P1));
  .send(L2, tell, initPos(P2));
  .send(L3, tell, initPos(P3));
  .send(L4, tell, initPos(P4));
  .send(L5, tell, initPos(P5));
  .send(L6, tell, initPos(P6));
  .send(L7, tell, initPos(P7));
  .send(L8, tell, initPos(P8));
  -notPosition.


// Coordinación

+stopTeam[source(X)]: team(100)
  <-
  ?unifiedList(L);
  .send(L, tell, holdPosition).


+keepMoving[source(X)]: team(100)
  <-
  ?unifiedList(L);
  .send(L, tell, continueMoving).


//Vuelta a la base

+goBackToBase[source(A)]: team(100)
  <-
  ?unifiedList(L);
  ?base(B);
  .send(L, tell, volver_a_la_base(B)).



// Pierde la bandera

+banderaPerdida[source(laQueSea)]: team(100)
  <-
  ?unifiedList(L);
  ?flag(F);
  .send(L, tell, bandera_perdida(F)).



// Mantenerse vivo y defenderse


+enemies_in_fov(ID,Type,Angle,Distance,Health,Position): health(H) > 60 & team(100)
  <-
  .shoot(10,Position).


