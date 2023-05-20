syms x y theta1(t) theta2(t) Lp Ld  d phi1(t) phi2(t) Mt Mp Md Jmp Jmd omegad th1 th2 dth1 dth2 ddth1 ddth2
% vinkler i robot for aktiv og passiv joints og endeffector punkt

Lp = 0.373;
Ld = 0.36;
Mp = 0.1792;
Md = 0.305;
d = 0.30;

Lp = 37.3;
Ld = 36;
d = 30;
Mp = 179.2;
Md = 305;
Jmp = Mp*Lp*1/12;
Jmd = Md*Ld*1/12;




%FVarIn = {th1 th2};
%FVarOut = {theta1(t) theta2(t)};
%%vinkler kætter på det er radianer

%Det er dem her der skal bruges
%Pxs = subs(Px, FVarOut, FVarIn)
%Pys = subs(Py, FVarOut, FVarIn)


%% invers kinematic
x = 0;
y = 61;

OP = [x; y];
OA = [-d/2;0];
OC = [d/2;0];
AP = OP-OA;
CP = OP-OC;

invAlfa1 = atan(AP(2)/AP(1));
invAlfa2 = atan(-CP(2)/CP(1));
invBeta1 = acos((norm(AP)^2+Lp^2-Ld^2)/(2*norm(AP)*Lp));
invBeta2 = acos((norm(CP)^2+Lp^2-Ld^2)/(2*norm(CP)*Lp));
invth1 = invAlfa1+invBeta1;
invth2 = pi-invAlfa2-invBeta2;

invth1 = invth1 * (180/pi);
invth2 = invth2 * (180/pi);

invth1 = invth1 + 99.0608
invth2=  invth2 + 114.1292

%% Beregninger

vinkel1 = 106.5992-205.66
vinkel2 = 73.4008-187.53

%%
%invers kinematic
xpoints = [0, 0, 2, 0, -1, -3, -1, 1, 0, 0];
ypoints = [49, 52, 54, 57, 59, 61, 64, 67, 69, 70];
listinvth1 = [];
listinvth2 = [];

for c = 1:length(xpoints)

    x = xpoints(c);
    y = ypoints(c);

OP = [x; y];
OA = [-d/2;0];
OC = [d/2;0];
AP = OP-OA;
CP = OP-OC;

invAlfa1 = atan(AP(2)/AP(1));
invAlfa2 = atan(-CP(2)/CP(1));
invBeta1 = acos((norm(AP)^2+Lp^2-Ld^2)/(2*norm(AP)*Lp));
invBeta2 = acos((norm(CP)^2+Lp^2-Ld^2)/(2*norm(CP)*Lp));
invth1 = invAlfa1+invBeta1;
invth2 = pi-invAlfa2-invBeta2;
invth1 = invth1 * 180/pi
invth2 = invth2 * 180/pi

listinvth1 = [listinvth1, invth1];
listinvth2 = [listinvth2, invth2];


end
%% Forward
th1 = 2.2;
th2 = 1.3;
theta = [th1; th2];
%phi = [phi1(t); phi2(t)];
Lp = 37.3;
Ld = 36;
d = 30;
% Forward kinemartic 

a = sqrt(d^2 + Lp^2 - 2*d*Lp*cos(th1));
alfa = acos((a^2+Lp^2-d^2)/(2*a*Lp));
beta = pi - th1 - alfa;
betamaerke = pi - beta - th2;
b = sqrt(Lp^2 + a^2 - 2*Lp*a*cos(betamaerke));
alfamaerke = acos((a^2+b^2-Lp^2)/(2*a*b));
alfasum=alfa+ alfamaerke;
alfamaerkemaerke = acos((b^2+Ld^2-Ld^2)/(2*b*Ld));
delta = alfasum + alfamaerkemaerke;
c = sqrt(Lp^2 + Ld^2 - 2*Lp*Ld*cos(delta));
betamaerkemaerke = acos((c^2+Ld^2-Lp^2)/(2*c*Ld));
gamma = pi - delta - betamaerkemaerke;
thetaxy = th1 - gamma;
Px = cos(thetaxy)*c-d/2;
Py = sqrt(c^2-Px^2);
F = [Px;Py];