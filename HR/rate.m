%% 
res=0;
t=t-min(t);

for i = [x, y, z]
    
    plot(t,i,'r');
    title('raw data');
    
    % cubic interpolation
    intervation=1000/256;
    xx=min(t):intervation:max(t);
    yy=spline(t,i,xx);
    
     figure
     plot(xx,yy);
     title('cubic interpolation');
%%
    % moving average filter
    output = tsmovavg(yy,'s',3,2);
    yy = yy';
    output = output';
    output(1:2)=[]; % remove first two NaN data
    %% butterworth filter
    n = 4;
    Wn = [10/128 13/128];
    [b,a] = butter(n,Wn);
    filt = filter(b,a,output);
    res=filt.^2+res;
end
   
%% normalisation 3 dimensions
r=sqrt(res);

%% butterworth filter
n = 2;
Wn = [0.75/128 2.5/128]; % normalisation
[b,a] = butter(n,Wn);
filt = filter(b,a,r);

figure 
plot(xx(3:length(xx)),filt);
title('2nd butterworth result');
%% fft
f=fft(filt);
f(1)=[]; % remove the first component which is the sum of data
n=length(f);
power = abs(f(1:floor(n/2))).^2;
nyquist = 1/2;
freq = (1:n/2)/(n/2)*nyquist;
period = 1./freq;

% plot
figure
plot(period,power);
set(gca,'xlim',[1 800]); 
title('fft result');
hold on;
index = find(power == max(power)); % find the one with strongest frequency
mainPeriodStr = num2str(period(index));
plot(period(index),power(index),'r.', 'MarkerSize',25); % plot the highest point
text(period(index)+2,power(index),['Period = ',mainPeriodStr]);
hold off;
result=60000/(period(index)*intervation); % heart rate result