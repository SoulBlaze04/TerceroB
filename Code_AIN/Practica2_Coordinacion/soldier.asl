// TEAM_ALLIED

+mando_recargas(R) : team(100)
  <-
  +recarga(R).

+mando_medicos(M) : team(100)
  <-
  +medicos(M).

+flag(F): team(100) & not(initial)
  <-
  +notPosition;
  .register_service("allied");
  .register_service("soldier");
  .print("Soldado registrado");
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
  .print("Soldado envia");
  .send(G, tell, estoy_en_posicion).


+reachingFinalPoint[source(A)]: team(100) 
  <-
  ?position(P);
  ?base(B);
  ?flag(F);
  .print(P);
  .getFinalPosition(P,B,F,X);
  +destination(X);
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


+holdPosition[source(G)]: team(100)
  <-
  ?destination(Dest);
  .stop;
  +continue(Dest).

+continueMoving[source(G)]: team(100)
  <-
  +retomaMovimiento;
  ?destination(D);
  +continue(D).

+continue(Destino): retomaMovimiento & team(100)
  <-
  .goto(Destino);
  -continue(Destino);
  -retomaMovimiento.


// Pide salud o munición

+health(H): team(100) & H < 50 & not(pidiendoayuda)
  <-
  +pidiendoayuda;
  .print("Necesito curarme");
  ?medicos(M);
  +searchMedics(M).

+ammo(A): team(100) & A < 50 & not(pidiendoayuda)
  <-
  +pidiendoayuda;
  .print("Necesito balas");
  ?recarga(T);
  +searchFieldops(T).

+searchMedics(M): team(100) & pidiendoayuda
  <-
  .print(M);
  ?position(P);
  +ofertas([]);
  +agentes([]);
  .send(M, tell, mandar_oferta(P));
  .wait(500);
  +elegir_agente_mas_cercano;
  -myMedics(_).

+searchFieldops(M): team(100) & pidiendoayuda
  <-
  ?position(P);
  .print(M);
  +ofertas([]);
  +agentes([]);
  .send(M, tell, mandar_oferta(P));
  .wait(500);
  +elegir_agente_mas_cercano;
  -myFieldops(_).

+oferta(P)[source(A)]: team(100) & pidiendoayuda
  <-
  ?ofertas(Aux);
  .concat(Aux, [P], Nuevasofertas);
  -+ofertas(Nuevasofertas);
  ?agentes(Agentes);
  .concat(Agentes, [A], Nuevosagentes);
  -+agentes(Nuevosagentes);
  .print("Recibida oferta y agente");
  -oferta(P).

+elegir_agente_mas_cercano: team(100) & ofertas(Ofertas) & agentes(Agentes) & pidiendoayuda
  <-
  ?position(P);
  .mas_cercano([Ofertas, Agentes, P], Tupla);
  .length(Tupla, L);
  if(L > 0){
    .nth(0, Tupla, Oferta);
    .nth(1, Tupla, Agente);
    .nth(2, Tupla, Indice);
    .delete(Indice, Agentes, Rechazaragentes);
    .send(Agente, tell, oferta_aceptada(Oferta));
    .send(Rechazaragentes, tell, oferta_rechazada);
    -+ofertas([]);
    -+agentes([]);
  };
  if(L < 1){
    -pidiendoayuda;
    .print("No hay agentes disponibles");
    ?flag(Y);
    .goto(Y);
  }.

+paquete_dejado(P)[source(A)]: team(100) & pidiendoayuda
  <-
  ?position(B);
  .print("Yendo a por el paquete");
  +posicion_inicial(B);
  +yendo_paquete;
  .goto(P).

+packs_in_fov(ID,Type,Angle,Distance,Health,Position) : team(100) & pidiendoayuda & yendo_paquete & not(paquete) & not(Type == 1003)
  <-
  +paquete;
  .goto(Position).

+target_reached(T): team(100) & yendo_paquete & pidiendoayuda
  <- 
  -yendo_paquete;
  ?posicion_inicial(P);
  +paquete_recogido;
  -posicion_inicial(_);
  -paquete;
  .goto(P).

+target_reached(T): team(100) & paquete_recogido & pidiendoayuda
  <- 
  -paquete_recogido;
  -pidiendoayuda;
  ?flag(P);
  .goto(P).

+paquete_en_posicion(P)[source(A)]: team(100) & pidiendoayuda
  <-
  ?position(B);
  +volver_posicion(B);
  .goto(P).

+pack_taken(N, T): team(100) & paquete & pidiendoayuda & not(T == 1003)
  <-
  ?flag(F);
  -pidiendoayuda;
  -yendo_paquete;
  -paquete;
  .print("Paquete recogido");
  .goto(F).

+pack_taken(N, T): team(100) & paquete & pidiendoayuda & not(T == 1003)
  <-
  ?base(F);
  .print("Bandera recogida");
  .goto(F).

// Dispara

+enemies_in_fov(ID,Type,Angle,Distance,Health,Position): health(H) & H > 25 & ammo(A) & A > 25 & not(pidiendoayuda) & not(volver_a_la_base(_))
  <-
  //+helpShooting;
  //?general(G);
  //.send(G, tell, get_backups);
  .shoot(7,Position).

+enemies_in_fov(ID,Type,Angle,Distance,Health,Position): health(H) & H > 25 & ammo(A) & A > 25 & not(pidiendoayuda) & not(hasFlag) & not(volver_a_la_base(_))
  <-
  //+helpShooting;
  //?general(G);
  //.send(G, tell, get_backups);
  .shoot(7,Position).

//+tryToHelp[source(G)]: team(100) & not(helpShooting)
  //<-
  //+helpShooting;
  //.turn(0.125);
  //.turn(-0.250);
  //.turn(0.125);


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

+bandera_perdida(F)[source(A)] : team(100)
  <-
  -volver_a_la_base(_);
  .goto(F).