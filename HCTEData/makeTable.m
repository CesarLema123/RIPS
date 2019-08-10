function [outputArg1,outputArg2] = makeTable(fileName)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

array = readmatrix(fileName);

sz = size(array);

array = readmatrix(fileName);

sz = size(array);


for j = 1:sz(1)
    fprintf('%3g & %3g & %3g & %3g \\\\ \n', array(j,3),array(j,4),array(j,1) ...
        , array(j,2))
    
end
    


end

