library(readxl)
library(EpiEstim)



cases <- read_excel("D:/mywork/SEIR_sim/新增data/无措施新增.xlsx")


fit=estimate_R(incid = cases[,2], 
                 method = "parametric_si",
                 config = make_config(list(mean_si=3.42,std_si=1.09)))

  

mean1<-fit[["R"]][["Mean(R)"]]
lower1<-fit[["R"]][["Quantile.0.025(R)"]]    
upper1<-fit[["R"]][["Quantile.0.975(R)"]]  
df<-data.frame(mean1,lower1,upper1)

#write.csv(df,file="D:/mywork/SEIR_sim/Rt_varied/Rt_v0.csv")