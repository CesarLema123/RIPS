function [blah] = bulkModTable
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

for k = 10:10:100
    fileName = num2str(k, 'bulkModuliData%2g.csv');
    array = readmatrix(fileName);

    sz = size(array);


    for j = 1:sz(1)
        for i = sz(2)-1:-1:1
            if i == 2
                array(j,i) = round(array(j,i),1,'significant');
            elseif i == 1
                digits = floor(log10(abs(array(j,i+1))+1));
                array(j,i) = round(array(j,i),-digits);
                fprintf('%10g & ', array(j,i))
            else
                %if j == 1
                    fprintf('%3g & %6g & ', k, array(j,i))    
                %else
                %    fprintf(' & %6g & ', array(j,i))
                %end
            end
        end
        fprintf('%.0e \\\\  \n', array(j,2))
    end
end

