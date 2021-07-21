import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel (r'.\beta.xlsx', converters={'序号':str,'R0':float,'Q0':float})
R0 = df['R0'][0]
Q0 = df['Q0'][0]
maskrate = 0
gamma = 1/14
alpha = 1/4
beta = R0*gamma

E = 0.728                       # 疫苗接种有效率
S0 = 1868                         # 人群总数(万人)
V = 0.1364*S0                    # 疫苗接种人数(万人)(用广州接种人数和荔湾广州人口比例计算)1000-745.18
SI = V*E                        # 疫苗接种有效者人数

time = 150                      # 传播时间(天)

I0 = 0.0001                    # 感染者人数(万人)
E0 = 0
R1 = 0
St = S0-SI-E0-I0-R1
X0 = (St, E0, I0, R1)
#Q0 = 0


def SEIR(X_init,_):
    Y = np.zeros(4)
    X = X_init
    Y[0] = -beta*X[0]*X[2]/S0
    Y[1] = beta*X[0]*X[2]/S0 - alpha*X[1]   #E
    Y[2] = alpha*X[1] - gamma*X[2]          #I
    Y[3] = gamma*X[2]                       #R
    return Y



t_range = np.arange(0, 2)
SEIR_Result = spi.odeint(SEIR, X0, t_range)
Xt = SEIR_Result[1, :]
#print(beta)
for t in range(1, time + 1):
    if t < len(df['R0']):
        #print(R0)
        R0 = df['R0'][t]
        Q0 = df['Q0'][t]
        beta = R0*gamma
    #print(beta)
    new_SEIR_Result = spi.odeint(SEIR, Xt, t_range)
    Xt = new_SEIR_Result[1, :]
    SEIR_Result = np.concatenate((SEIR_Result, new_SEIR_Result[1:, :]))

plt.plot(SEIR_Result[:,1] * 10000,color = 'orange',label = 'E',marker = '.')
plt.plot((SEIR_Result[:,2]+SEIR_Result[:,3]) * 10000,color = 'red',label = 'I+R',marker = '.')
#plt.plot(SEIR_Result[:,0] * 10000,color = 'green',label = 'R',marker = '.')
plt.title('SEIR')
plt.legend()
plt.xlabel('Time /day')
plt.ylabel('Number')
plt.show()



#print(np.where(SEIR_Result[:,2] == np.amax(SEIR_Result[:,2])))
#print(np.amax(SEIR_Result[:,2])*10000)
for t in range(0,time):
    print((SEIR_Result[t,2] + SEIR_Result[t,3])*10000)
    if t==1:
        if (((SEIR_Result[t,2] + SEIR_Result[t,3])*10000)-(SEIR_Result[t-1,2] + SEIR_Result[t-1,3])*10000)<1:
            print("end");
            print((SEIR_Result[t,2] + SEIR_Result[t,3])*10000)
            break
