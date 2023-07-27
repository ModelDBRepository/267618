% Determine the number of spikes given an array of spike train
function countSpike = firingRate(spikeTrain)
    threshold = -50;
    aboveThresholdFlag = false;
    aboveThresholdSpikes = [];
    countSpike = 0;
    for i = 1:length(spikeTrain)
        if spikeTrain(i) > threshold
            aboveThresholdFlag = true;
            aboveThresholdSpikes = [aboveThresholdSpikes, spikeTrain(i)];
        else
            if aboveThresholdFlag
                if abs(max(aboveThresholdSpikes)-spikeTrain(i)) > 40
                    countSpike = countSpike + 1;
                end
            end
            aboveThresholdFlag = false;
            aboveThresholdSpikes = [];
        end
    end
end