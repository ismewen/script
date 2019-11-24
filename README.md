## kobe
Remembering lots of product k8s commands can be a bit annoying.Have no fear, *Kobe* is here 

## usage

`kobe + namespace` such as kobe mysql-5432. Flowing are the output you will see

```
0:kubectl get pods -n mysql-5432
1:kubectl get ingress -n mysql-5432
2:kubectl get secrets -n mysql-5432
3:kubectl get certificate -n mysql-5432
4:kubectl get statefulset -n mysql-5432
5:kubectl get pv -n mysql-5432
6:kubectl get pvc -n mysql-5432
7:kubectl exec -it mysql-5432-db-0 -c mysql-agent -n mysql-5432 bash
8:kubectl exec -it mysql-5432-db-0 -n mysql-5432 bash
9:kubectl describe pods/mysql-5432-db-0 -n mysql-5432
10:kubectl describe ingress/name -n mysql-5432
11:kubectl describe secrets/name -n mysql-5432
12:kubectl describe certificate/name -n mysql-5432
13:kubectl describe statefulset/name -n mysql-5432
14:kubectl describe pv/name -n mysql-5432
15:kubectl describe pvc/name -n mysql-5432
16:kubectl edit pods/mysql-5432-db-0 -n mysql-5432
17:kubectl edit ingress/name -n mysql-5432
18:kubectl edit secrets/name -n mysql-5432
19:kubectl edit certificate/name -n mysql-5432
20:kubectl edit statefulset/name -n mysql-5432
21:kubectl edit pv/name -n mysql-5432
22:kubectl edit pvc/name -n mysql-5432
```
then input your choice to execute related command

## Congratulations
Congratulations! When you read here, you have know everything about kobe. 当然, 任何问题或者改进建议请随时和我联系