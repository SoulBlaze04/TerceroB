// TEAM_ALLIED 

+flag(F): team(100) & not(initial)
  <-
  +notPosition;
  .register_service("allied");
  .register_service("fieldop");
  .print("Fieldop registrado");
  .wait(5000);
  .get_service("general");
  .get_service("comandante");
  .get_medics;
  .get_fieldops;
  .get_service("soldier");
  +initial.

+initPos(P)[source(G)]: team(100)
  <-
  .print(P);
  .goto(P).

+target_reached(P) : team(100) & notPosition
  <-
  -notPosition;
  ?general(G);
  .print("Fieldop envia");
  .send(G, tell, estoy_en_posicion).


+reachingFinalPoint[source(A)]: team(100) 
  <-
  ?position(P);
  ?base(B);
  ?flag(F);
  .print(P);
  .getFinalPosition(P,B,F,X);
  .goto(X);
  +initGeneral.
  

+initGeneral: team(100) & not(reachingFinalPoint)
  <-
  +gettingFlag;
  ?flag(F);
  .goto(F);
  -initGeneral.

+flag(F): team(100) & not(reachingFinalPoint)
  <-
  +gettingFlag;
  .goto(F).

+holdPosition[source(G)]: not(helpShooting) 
  <-
  ?destination(Dest);
  .stop;
  +continue(Dest).

+keepMoving[source(G)]: team(100)
  <-
  +retomaMovimiento.

+continue(Destino): retomaMovimiento & team(100)
  <-
  .goto(Destino);
  -continue(Destino);
  -retomaMovimiento.


// Manda munición

+mandar_oferta(P)[source(A)]: team(100) & not(ayudando)
  <-
  ?position(B);
  .send(A, tell, oferta(B));
  +ayudando;
  -mandar_oferta(P).

+oferta_aceptada(P)[source(A)]: team(100) & ayudando
  <-
  +dejando_paquete;
  ?position(B);
  +posicion_inicial(B);
  +ayudado(A);
  .goto(P).

+mandar_oferta(P)[source(A)]: team(100) & ayudando
  <-
  .print("No disponible").

+target_reached(T): team(100) & dejando_paquete
  <- 
  .reload;
  ?ayudado(A);
  -ayudado(A);
  ?position(B);
  .send(A, tell, paquete_dejado(B));
  -dejando_paquete;
  ?flag(P);
  -posicion_inicial(_);
  .goto(P).

+target_reached(T): team(100) & ayudando & not(dejando_paquete)
  <- 
  -ayudando.


// Dispara

+enemies_in_fov(ID,Type,Angle,Distance,Health,Position)
  <-
  //+helpShooting;
  .shoot(7,Position).


// Bandera conseguida

+flag_taken: team(100)
  <-
  +hasFlag;
  .print("Bandera_recogida");
  ?general(G);
  .send(G, tell, goBackToBase).

+volver_a_la_base(B)[source(A)]: team(100)
  <- 
  .goto(B).

+enemies_in_fov(ID,Type,Angle,Distance,Health,Position): not(pidiendoayuda) & volver_a_la_base(_) & not(friends_in_fov(_,_,_,_,_,_)) & not(hasFlag)
  <-
  .shoot(7,Position).

// Pierde la bandera

+queMeMueroConBandera: hasFlag & health(H) & H < 5 & team(100)
  <-
  ?general(G);
  .send(G, tell, banderaPerdida);
  -hasFlag.

+ammo(H): team(100) & H < 25
  <-
  .reload;
  +autocura.

+packs_in_fov(ID,Type,Angle,Distance,Health,Position) : team(100)
  <-
  .goto(Position).

+packs_in_fov(ID,Type,Angle,Distance,Health,Position) : team(100) & pidiendoayuda & not(paquete)
  <-
  +paquete;
  .goto(Position).

+packs_in_fov(ID,Type,Angle,Distance,Health,Position) : team(100) & autocura & not(paquete)
  <-
  +paquete;
  .goto(Position);
  -paquete;
  ?flag(F);
  .goto(F).

+bandera_perdida(F)[source(A)] : team(100)
  <-
  -volver_a_la_base(_);
  .goto(F).