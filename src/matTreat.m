


M = csvread('../data/trds.csv',1,1);
order = M(:,1);
depsN = M(:,2);
score = M(:,3);
clear M;
share = csvread('../data/ctd.csv');
%%


figure(1)
plot(order,score,'b.')
set(gca,'yscale','log')
xlabel('Ordering')
ylabel('Score')
title('Transitive Dependency Score (paths)')

total = (repmat(depsN,1,size(depsN,1)) + repmat(depsN',size(depsN,1),1)) - share;
frac = share./total;

[X, Y] = meshgrid(order,order);
figure(2)
imshow(frac)
%surf(frac,'LineStyle','none')