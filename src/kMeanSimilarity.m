function [ clusters, startPoints ] = kMeanSimilarity( similarity, selector )
%

data = similarity;
startPoints = selector(data);
numP = size(startPoints,1);
%clusterCenters = cell(101,1);
%clusterCenters{1} = startPoints;


clusters = zeros(1,size(data,1));
for sp = 1:numP
    clusters(startPoints(sp)) = sp;
end
sim = zeros(size(clusters));

check = 1;
%L2like = @(diff) sum(diff.^2,1);
for i = 1:100
    % M-phase
    for c = 1:numP
        sim(c,:) = sum(similarity(clusters == c,:),1)./sum(clusters == c);
    end
    %diff = calcMetric(data',clusterCenters{i}',L2like);
    [~,newClusters] = max(sim,[],1);
    
    if newClusters == clusters
        check = 0;
        break;
    else
        clusters = newClusters;
    %    % E-phase
    %    for j = 1:numP
    %        clusterCenters{i+1}(j,:) = sum(data(clusters==j,:))/sum(clusters==j);
    %    end
    end
end
i  = i + check;
% check if we ran to the limit
%if size(clusterCenters{101},1)
%    i = 101;
%end
%clusterCenters = clusterCenters(1:i);
%finalCenters = clusterCenters{end};
clusters = clusters';

end

