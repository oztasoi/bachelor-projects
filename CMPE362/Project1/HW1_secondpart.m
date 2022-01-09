%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 7 %
mysignal = load('mysignal.mat'); %loaded the audio data
fftY = fft(mysignal.x); % converted raw data via 'Discrete Fast Fourier Transform'
fftshiftY = fftshift(fftY); % shifted the base value to show the negative parts and the positive parts of the signal as counterparts
n = length(mysignal.x); % found the sample size
f = (-n/2:n/2-1) * (mysignal.fs/n); % created the symmetric frequency axis to plot
power = (abs(fftshiftY) .^2 ) / n; % took the normalized power of signal
figure('Name', 'Question7', 'Color', 'Yellow');
plot(f, power); % plot the signal via freq-power tuples
xlabel('frequency(hz)');
ylabel('power(mW)');
% Problem 7 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 8 %
[favSong, fs] = audioread('slash.mp3'); % loaded the favsong
favSongData = favSong(:,1) + favSong(:,2) ./ 2; % since it is a stereo recorded song, I've taken the average of different signal layers.
n = length(favSongData); % found the sample size
favSongFFT = fft(favSongData); % transformed data under 'Discrete Fast Fourier Transform'
favSongFFTShift = fftshift(favSongFFT); % shifted the FFT data to show the counterparts of each signal
f = (-n/2:n/2-1) * (fs/n); % created the symmetric frequency axis
time = (0:5/n:5-5/n); % created the time axis
power = abs(favSongFFTShift) .^2 / n; % took the normalized power of the signal
figure('Name', 'Favorite Song FFTShift Power-Frequency Plot', 'Color', 'Yellow');
plot(f, power); % plotted the freq-power graph
xlabel('frequency(hz)');
ylabel('Power(dBm)');
figure('Name', 'Favorite Song Amplitude-Time Plot', 'Color', 'Yellow');
plot(time, favSongData); % plotted the time-amplitude graph
xlabel('time(sec)');
ylabel('Amplitude');
% Problem 8 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
% Problem 9 %
lena_transform = imread('lena.png'); % read the image as 3D matrix with RGB values.
lena_gray_transform = rgb2gray(lena_transform); % transformed each RGB value into single grayscale value.
lena_mean = mean(lena_gray_transform, 'all'); % took the mean of grayscale matrix
disp("Mean: " + lena_mean);
lena_gray_array = double(lena_gray_transform(:));
lena_standard_deviation = std(lena_gray_array);
disp("Standard deviation: " + lena_standard_deviation);
[MIN, INMIN] = min(lena_gray_transform); % found the minimum value of each column and its indexes
[min, inmin] = min(MIN); % found the overall minimum value and its index
disp("Minimum element value: " + min);
disp("Minimum element position(row, column): " + INMIN(inmin) + " " + inmin);
[MAX, INMAX] = max(lena_gray_transform); % found the maximum value of each column and its indexes
[max, inmax] = max(MAX); % found the overall maximum value and its index
disp("Maximum element value: " + max);
disp("Maximum element position(row, column): " + INMAX(inmax) + " " + inmax);
% Problem 9 Ending %
%%%%%%%%%%%%%%%%%%%%%%%%%