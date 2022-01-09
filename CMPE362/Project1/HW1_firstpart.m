%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 1%
t = (-2:0.01:2);
y1 = sin(2*pi*t);
y2 = sin(2*pi*t*10);
y3 = 10*sin(2*pi*t);
y4 = sin(2*pi*t)+10;
y5 = sin(2*pi*(t-0.5));
y6 = 10*sin(2*pi*t*10);
y7 = t.*sin(2*pi*t);
y8 = sin(2*pi*t) ./ t;
y9 = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8;
figure('Name', 'Question1', 'Color', 'Yellow');
subplot(5,2,1), plot(t, y1); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,2), plot(t, y2);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,3), plot(t, y3);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,4), plot(t, y4);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,5), plot(t, y5);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,6), plot(t, y6);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,7), plot(t, y7);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,8), plot(t, y8);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,9), plot(t, y9);
xlabel('time(sec)');
ylabel('value');
% Problem 1 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 2 %
rand_vector1 = randn(1,401);
z = rand_vector1 .* 0.1;
y10 = z;
y11 = z + t;
y12 = z + y1;
y13 = z .* y1;
y14 = t .* sin(2 * pi .* z);
y15 = sin(2 * pi * (t + z));
y16 = z .* y2;
y17 = sin(2 * pi * (t + 10 .* z));
y18 = y1 ./ z;
y19 = y11 + y12 + y13 + y14 + y15 + y16 + y17 + y18;
figure('Name', 'Question2', 'Color', 'Yellow');
subplot(5,2,1), plot(t, y10); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,2), plot(t, y11); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,3), plot(t, y12); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,4), plot(t, y13); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,5), plot(t, y14); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,6), plot(t, y15); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,7), plot(t, y16); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,8), plot(t, y17); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,9), plot(t, y18); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,10), plot(t, y19); 
xlabel('time(sec)');
ylabel('value');
% Problem 2 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 3 %
rand_vector2 = rand(1, 401);
z = rand_vector2 .* 0.1;
y20 = z;
y21 = z + t;
y22 = z + y1;
y23 = z .* y1;
y24 = t .* sin(2 * pi * z);
y25 = sin(2 * pi * (t + z));
y26 = z .* y2;
y27 = sin(2 * pi * (t + 10 .* z));
y28 = y1 ./ z;
y29 = y21 + y22 + y23 + y24 + y25 + y26 + y27 + y28;
figure('Name', 'Question3', 'Color', 'Yellow');
subplot(5,2,1), plot(t, y20);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,2), plot(t, y21);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,3), plot(t, y22);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,4), plot(t, y23);
xlabel('time(sec)');
ylabel('value');
subplot(5,2,5), plot(t, y24); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,6), plot(t, y25); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,7), plot(t, y26); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,8), plot(t, y27); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,9), plot(t, y28); 
xlabel('time(sec)');
ylabel('value');
subplot(5,2,10), plot(t, y29); 
xlabel('time(sec)');
ylabel('value');
% Problem 3 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 4 %
rand_vector3 = randn(1, 5000);
r1 =  rand_vector3;
r2 = sqrt(8) .* rand_vector3;
r3 = sqrt(64) .* rand_vector3;
r4 = sqrt(256) .* rand_vector3;
figure('Name', 'Question4', 'Color', 'Yellow');
subplot(2,2,1), histogram(r1);
xlabel('mean');
ylabel('quantity');
subplot(2,2,2), histogram(r2);
xlabel('mean');
ylabel('quantity');
subplot(2,2,3), histogram(r3);
xlabel('mean');
ylabel('quantity');
subplot(2,2,4), histogram(r4);
xlabel('mean');
ylabel('quantity');
% Problem 4 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 5 %
rand_vector3 = randn(1, 5000);
r6 = 10 + rand_vector3;
r7 = 20 + sqrt(4) .* rand_vector3;
r8 = -10 + rand_vector3;
r9 = -20 + sqrt(4) .* rand_vector3;
figure('Name', 'Question5', 'Color', 'Yellow');
subplot(2,2,1), histogram(r6);
xlabel('mean');
ylabel('quantity');
subplot(2,2,2), histogram(r7);
xlabel('mean');
ylabel('quantity');
subplot(2,2,3), histogram(r8);
xlabel('mean');
ylabel('quantity');
subplot(2,2,4), histogram(r9);
xlabel('mean');
ylabel('quantity');
% Problem 5 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 6 %
rand_vector4 = rand(1, 5000);
r11 = -4 + 8 .* rand_vector4;
r21 = -20 + 40 .* rand_vector4;
figure('Name', 'Question6', 'Color', 'Yellow');
subplot(2,1,1), histogram(r11);
xlabel('mean');
ylabel('quantity');
subplot(2,1,2), histogram(r21);
xlabel('mean');
ylabel('quantity');
% Problem 6 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%