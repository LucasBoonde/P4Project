
% Create figure windows for each plot
figure(1);
xlabel('t');
ylabel('q');
legend('theta')
title('Position (deg)');

figure(2);
xlabel('t');
ylabel('qdot');
title('Velocity (deg / sec)');

figure(3);
xlabel('t');
ylabel('qdotdot');
title('Acceleration (deg / sec^2)');

%Tidsintervaller mellem punkterne
ts =        [0, 10, 20, 30, 40, 50, 60, 70];


%Points for theta1:
points1 = [1.8629, listinvth1]; %listinvth kommer fra inverskinematic
%points1 = [1.5957, 1.5957, 1.5957]
%Points for theta2:
points2 = [1.2870,  listinvth2];
%points2 = listinvth2;
pointsdot1 = [0, 0, 0, 0, 0, 0, 0, 0];
pointsdot2 = [0, 0, 0, 0, 0, 0, 0, 0];




%Længden af Arrayet for punkterne
L1 = length(points1);
L2 = length(points2);
Ti = 0.2; %Sample Time

n = length(ts);
diffs= diff(ts)/Ti;
BT=max( diffs(diffs>=0) );
listq1= zeros(numel(round(diffs)),round(BT));
listq2=zeros(numel(round(diffs)),round(BT));
listdq1 = zeros(numel(round(diffs)),round(BT)); 
listdq2 = zeros(numel(round(diffs)),round(BT));
listddq1 = zeros(numel(round(diffs)),round(BT));
listddq2 = zeros(numel(round(diffs)),round(BT));
%Function that calculates the trajectory for x points1
for c = 1:L1-1
    tstart = ts(c);
    tfinal = ts(c+1);
    T = tfinal - tstart;
    
    
    %For pos og hastighed for initial punkt
    theta0 = points1(c);
    thetaf = points1(c+1);

    %For pos og hastighed for final punkt
    thetad0 = pointsdot1(c);
    thetadf = pointsdot1(c+1);
    
     
    if tstart ~= 0
        a0 = theta0;
        a1 = thetad0;
        a2 = (-3 * (theta0 - thetaf) - (2 * thetad0+thetadf )*(tfinal - tstart))/ (tfinal - tstart) .^ 2;
        a3 = (2 * (theta0 - thetaf) + (thetad0+thetadf )*(tfinal - tstart))/ (tfinal - tstart) .^ 3;
        %a2 = 3/tfinal.^2*T-2/tfinal*thetad0-1/tfinal*thetadf;
        %a3 = -2/tfinal.^3*T+1/tfinal.^2*(thetadf+thetad0);
        
        %t = linspace(tstart,tfinal, 100);
        t = linspace(0, T, T/Ti); %Mangler måske rigtig samplingstid
        disp(t(c))
       
        %Funktionerne der beskriver pos, vel og acc
        q = a0+a1*t+a2*t.^2+a3*t.^3;
        qdot = a1+2*a2*t+3*a3*t.^2;
        qdotdot = 2*a2+6*a3*t;
        

    end
            
    if tstart == 0
        a0 = theta0;
        a1 = thetad0;
        a2 = (-3 * (theta0 - thetaf) - (2 * thetad0+thetadf )*tfinal)/ tfinal^ 2;
        a3 = (2 * (theta0 - thetaf) + (thetad0+thetadf)*tfinal)/ tfinal^ 3;
        
        %t = linspace(tstart,tfinal, 100);
        t = linspace(0, tfinal, T/Ti);
        disp(t(c));

        %Funktionerne der beskriver pos, vel og acc
        q = a0+a1*t+a2*t.^2+a3*t.^3;
        qdot = a1+2*a2*t+3*a3*t.^2;
        qdotdot = 2*a2+6*a3*t;
        
    end
    listq1(c, 1:diffs(c)) = q;
    listq1 = round(listq1,4);
    listdq1(c, 1:diffs(c)) = qdot;
    listdq1 = round(listdq1,4);
    listddq1(c, 1:diffs(c)) = qdotdot;
    listddq1 = round(listddq1,4);
    %qref = generateQMatrix(c,q);
    %disp(result);

    % Opdater Position plot
    figure(1);
    plot(t+ ts(c), q);
    xlabel('t');
    ylabel('q');
    title('Position (deg)');
    hold on
    
    %plot(ts(c),points1(c), 'o')
    

    % Opdater Velocity plot 1
    figure(2);
    plot(t+ ts(c), qdot);
    xlabel('t');
    ylabel('qdot');
    title('Velocity (deg / sec)');
    %plot(ts(c),pointsdot1(c), 'o');
    hold on;


    % Opdater Acceleration plot
    figure(3);
    plot(t+ ts(c), qdotdot);
    xlabel('t');
    ylabel('qdotdot');
    title('Acceleration (deg / sec^2)');
    hold on;
end

%Function that calculates the trajectory for x points2
for c = 1:L2-1
    tstart = ts(c);
    tfinal = ts(c+1);
    T = tfinal - tstart;
    
    
    %For pos og hastighed for initial punkt
    theta0 = points2(c);
    thetaf = points2(c+1);

    %For pos og hastighed for final punkt
    thetad0 = pointsdot2(c);
    thetadf = pointsdot2(c+1);
    
     
    if tstart ~= 0
        a0 = theta0;
        a1 = thetad0;
        a2 = (-3 * (theta0 - thetaf) - (2 * thetad0+thetadf )*(tfinal - tstart))/ (tfinal - tstart) .^ 2;
        a3 = (2 * (theta0 - thetaf) + (thetad0+thetadf )*(tfinal - tstart))/ (tfinal - tstart) .^ 3;
        %a2 = 3/tfinal.^2*T-2/tfinal*thetad0-1/tfinal*thetadf;
        %a3 = -2/tfinal.^3*T+1/tfinal.^2*(thetadf+thetad0);
        
        %t = linspace(tstart,tfinal, 100);
        t = linspace(0, T, T/Ti); %Mangler måske rigtig samplingstid
        disp(t(c))
       
        %Funktionerne der beskriver pos, vel og acc
        q = a0+a1*t+a2*t.^2+a3*t.^3;
        qdot = a1+2*a2*t+3*a3*t.^2;
        qdotdot = 2*a2+6*a3*t;
       
    end
    
    if tstart == 0
        a0 = theta0;
        a1 = thetad0;
        a2 = (-3 * (theta0 - thetaf) - (2 * thetad0+thetadf )*tfinal)/ tfinal^ 2;
        a3 = (2 * (theta0 - thetaf) + (thetad0+thetadf)*tfinal)/ tfinal^ 3;
        
        %t = linspace(tstart,tfinal, 100);
        t = linspace(0, tfinal, T/Ti);
        disp(t(c));

        %Funktionerne der beskriver pos, vel og acc
        q = a0+a1*t+a2*t.^2+a3*t.^3;
        qdot = a1+2*a2*t+3*a3*t.^2;
        qdotdot = 2*a2+6*a3*t;
        
    end
    listq2(c, 1:diffs(c)) = q;
    listq2 = round(listq2,4);
    listdq2(c, 1:diffs(c)) = qdot;
    listdq2 = round(listdq2,4);
    listddq2(c, 1:diffs(c)) = qdotdot;
    listddq2 = round(listddq2,4);
    %qref = generateQMatrix(c,q);
    %disp(result);

    % Opdater Position plot 2
    figure(1);
    plot(t+ ts(c), q);
    xlabel('t');
    ylabel('q');
    title('Position (deg)');
    hold on
    
    %plot(ts(c),points2(c), 'o')
    

    % Opdater Velocity plot 2
    figure(2);
    plot(t+ ts(c), qdot);
    xlabel('t');
    ylabel('qdot');
    title('Velocity (deg / sec)');
    %plot(ts(c),pointsdot2(c), 'o');
    hold on;


    % Opdater Acceleration plot 2
    figure(3);
    plot(t+ ts(c), qdotdot);
    xlabel('t');
    ylabel('qdotdot');
    title('Acceleration (deg / sec^2)');
    hold on;
end
writematrix(ts,'ts.txt') 
writematrix(listq1,'refq1.txt')
writematrix(listq2,'refq2.txt')
writematrix(listdq1,'refdq1.txt')
writematrix(listdq2,'refdq2.txt')
writematrix(listddq1,'refddq1.txt')
writematrix(listddq2,'refddq2.txt')