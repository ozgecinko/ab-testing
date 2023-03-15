#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor. A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor. Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.



#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.



#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.


import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

control_group = pd.read_excel('datasets/ab_testing.xlsx', sheet_name='Control Group')
test_group = pd.read_excel('datasets/ab_testing.xlsx', sheet_name='Test Group')

control_group.head()
test_group.head()


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

# Veriye genel bakış sağlayan fonksiyonu yazdım.
def check_df(dataframe, head=5):
    print("##### Shape #####")
    print(dataframe.shape)
    print("##### Info #####")
    print(dataframe.info())
    print("##### Types #####")
    print(dataframe.dtypes)
    print("##### Head #####")
    print(dataframe.head(head))
    print("##### Tail #####")
    print(dataframe.tail(head))
    print("##### NA #####")
    print(dataframe.isnull().sum())
    print("##### Quantiles #####")
    print(dataframe.describe().T)


check_df(control_group)
check_df(test_group)


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df = pd.concat([control_group, test_group], axis=0).reset_index()

check_df(df)

"""
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=False)
"""

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
# Test ve kontrol gruplarının satın alma oranı (purchase) arasında istatistiksel olarak anlamlı bir fark var mıdır?

# H0: M1 = M2, fark yoktur.
# H1: M1 != M2, fark vardır.

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

############################
# Varyans Homojenliği
############################

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen değildir.

df.groupby("Purchase").agg({"Earning": "mean"})

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.
control_group.groupby("Purchase").mean()
test_group.groupby("Purchase").mean()

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################
# p-value < ise 0.05 'ten H0 RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız. Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.

# Normallik Varsayımı
control_stat, p_control = shapiro(control_group['Purchase']) # Kontrol grubu için.
test_stat, p_test = shapiro(test_group['Purchase']) # Test grubu için.
p_val = 0.05 # 0.05 belirledik.

if p_control < p_val:
    print('Kontrol grubu normal dağılmamıştır. (p-value={})'.format(p_control))
else:
    print('Kontrol grubu normal dağılmıştır. (p-value={})'.format(p_control))


if p_test < p_val:
    print('Test grubu normal dağılmamıştır. (p-value={})'.format(p_test))
else:
    print('Test grubu normal dağılmıştır. (p-value={})'.format(p_test))

# Varyans Homojenliği
stat_levene, p_levene = levene(control_group['Purchase'], test_group['Purchase'])

if p_levene < p_val:
    print(f'İki grubun varyansı eşit değildir. (p-value={p_levene})')
else:
    print(f'İki grubun varyansı eşittir. (p-value={p_levene})')

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz
# İki grup için de varsayım sağlanmaktadır, T testine bakarız.
stat, p = ttest_ind(control_group['Purchase'], test_group['Purchase'], equal_var=True)

if p < p_val:
    print('İki grup arasında anlamlı bir fark vardır. (p-value={})'.format(p))
else:
    print('İki grup arasında anlamlı bir fark yoktur. (p-value={})'.format(p))


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
# Normallik varsayımı için shapiro,
# varyans homojenliği varsayımı için levene,
# çıkan sonuca göre T-testini kullandım.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
