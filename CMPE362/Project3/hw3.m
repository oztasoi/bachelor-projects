%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initialize the primary image, the effect kernels and the color channels
raw = imread('./jokerimage.png');

blur3 = [1, 1, 1, 1, 1, 1, 1, 1, 1]/9;
blurgaussian3 = [1, 2, 1, 2, 4, 2, 1, 2, 1]/16;
sharpen3 = [-1, -1, -1, -1, 9, -1, -1, -1, -1];
edge3 = [-1, -1, -1, -1, 8, -1, -1, -1, -1];
sobel3_v = [-1, 0, 1, -2, 0, 2, -1, 0, 1];
sobel3_h = [-1, -2, -1, 0, 0, 0, 1, 2, 1];
emboss3 = [-2, -1, 0, -1, 1, 1, 0, 1, 2];

red = raw(:, :, 1);
green = raw(:, :, 2);
blue = raw(:, :, 3);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Blur the primary image with normalized kernel blur3

blur_red = convolve3(red, blur3);
blur_green = convolve3(green, blur3);
blur_blue = convolve3(blue, blur3);

blur3_img = cat(3, blur_red, blur_green, blur_blue);
imwrite(blur3_img, 'blur3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Blur the primary image with Gaussian kernel blur3

blurg_red = convolve3(red, blur3);
blurg_green = convolve3(green, blur3);
blurg_blue = convolve3(blue, blur3);

blurg3_img = cat(3, blurg_red, blurg_green, blurg_blue);
imwrite(blur3_img, 'blurgaussian3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sharpen the blurred image with sharpen3 kernel

blurred_img = imread('./blur3joker.png');

sharpen3_red = convolve3(blurred_img(:, :, 1), sharpen3);
sharpen3_green = convolve3(blurred_img(:, :, 2), sharpen3);
sharpen3_blue = convolve3(blurred_img(:, :, 3), sharpen3);

sharpen3_img = cat(3, sharpen3_red, sharpen3_green, sharpen3_blue);
imwrite(sharpen3_img, 'sharpen3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Detect edges in the primary image with edge3 kernel

edge3_red = convolve3(red, edge3);
edge3_green = convolve3(green, edge3);
edge3_blue = convolve3(blue, edge3);

edge3_img = cat(3, edge3_red, edge3_green, edge3_blue);
imwrite(edge3_img, 'edge3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Detect sobel edges in the primary image with sobel3_v and sobel3_h
% kernels

sobel3_redv = convolve3(red, sobel3_v);
sobel3_redh = convolve3(red, sobel3_h);
sobel3_r = hyper(sobel3_redv, sobel3_redh);

sobel3_greenv = convolve3(green, sobel3_v);
sobel3_greenh = convolve3(green, sobel3_h);
sobel3_g = hyper(sobel3_greenv, sobel3_greenh);

sobel3_bluev = convolve3(blue, sobel3_v);
sobel3_blueh = convolve3(blue, sobel3_h);
sobel3_b = hyper(sobel3_bluev, sobel3_blueh);

sobel3_img = cat(3, sobel3_r, sobel3_g, sobel3_b);
imwrite(sobel3_img, 'sobel3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Emboss the primary image with emboss3 kernel

emboss3_red = convolve3(red, emboss3);
emboss3_green = convolve3(green, emboss3);
emboss3_blue = convolve3(blue, emboss3);

emboss3_img = cat(3, emboss3_red, emboss3_green, emboss3_blue);
imwrite(emboss3_img, 'emboss3joker.png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Convolution function implementation as convolve3 and norm finding function
% implementation as hyper. The convolution function can be used under the
% assumption of the kernel is exactly 3 by 3 matrix.

function hyped = hyper(rawx, rawy)
    % taking the norm value of the current pixel's vertical and horizontal
    % value
    x = double(rawx);
    y = double(rawy);
    hyped = sqrt(x .^ 2 + y .^ 2);
    hyped = uint8(hyped);
end

function conv = convolve3(rawx, y)
    % padding part of the input matrix
    k = double(zeros(length(rawx) + 2, length(rawx) + 2));
    x = double(rawx);
    k(2:length(rawx)+1, 2:length(rawx)+1) = x;
    x = k;
    % padding part of the input matrix finished
    % initialize the output matrix
    conv = double(zeros(length(x), length(x)));
    % initalize the output matrix finished
    for i=2:length(x)-1
        for j=2:length(x)-1
            index = (i-1) * length(x) + j;
            % convolution operation for one value in the matrix
            conv(index) = x((i-2) * length(x) + (j-1)) * y(1) + x((i-2) * length(x) + j) * y(2) + x((i-2) * length(x) + (j+1)) * y(3) + x((i-1) * length(x) + (j-1)) * y(4) + x((i-1) * length(x) + j) * y(5) + x((i-1) * length(x) + (j+1)) * y(6) + x((i) * length(x) + (j-1)) * y(7) + x((i) * length(x) + j) * y(8) + x((i) * length(x) + (j+1)) * y(9);
            % convolution operation for one value in the matrix finished
        end
    end
    % converted output matrix into 8 bit unsigned integer
    conv = uint8(conv(2:length(conv) - 1, 2:length(conv) - 1));
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%