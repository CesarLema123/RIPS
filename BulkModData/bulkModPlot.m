function [blah] = bulkModPlot
clf
for k = 10:10:100
    fileName = num2str(k, 'bulkModuliData%2g.csv');
    array = readmatrix(fileName);
    errorbar(array(:,3),array(:,1),array(:,2))
    hold on
end
legend ('10% Cu', '20% Cu','30% Cu','40% Cu','50% Cu','60% Cu' ...
    ,'70% Cu','80% Cu','90% Cu','100% Cu')
xlabel ('Volume (cubic Angstroms)')
ylabel ('Bulk Modulus (bars)')
end

