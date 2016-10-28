


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
frac = share./max(total,1);

[X, Y] = meshgrid(order,order);
figure(2)
imshow(frac)
%surf(frac,'LineStyle','none')

figure(3)
hist(frac(:))

cutoff = 0.9;
frac2 = max(frac > cutoff,diag(ones(size(depsN,1),1)));
[fracS, fracO] = sort(sum(frac2,2),'descend');


figure(4)
imshow(frac2)
figure(5)
plot(fracS)

clusterN = 20;
startClusters = zeros(clusterN,1);
i = 0;
for c = 1:clusterN
    searching = 1;
    while searching
        i = i + 1;
        if i > size(depsN,1)
            clusterN = c-1;
            break
        end
        notused = 1;
        for j = 1:c-1
            if frac2(startClusters(j),fracO(i)) > cutoff
                notused = 0;
                break;
            end
        end
        if notused
            searching = 0;
            startClusters(c) = fracO(i);
        end
    end
end

selector = @(x) startClusters;
[clusters, ~] = kMeanSimilarity(frac2,selector);


% show cluster
im = zeros(size(share,1),size(share,2),3);
colors = [1,0,0;
          0,1,0;
          0,0,1;
          1,1,0;
          1,0,1;
          0,1,1;
          1,1,1];
for c = 1:min(clusterN,6);
    points = clusters == c; % frac2(startClusters(c),:) > cutoff;
    im(points,points,1) = colors(c,1);
    im(points,points,2) = colors(c,2);
    im(points,points,3) = colors(c,3);
end

figure(6)
imshow(im)

