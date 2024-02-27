[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/RvxJKA0f)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=13264693)

Primero tenemos main y dev.

Luego el resto de ramas propias: dev_cls, dev_ibt, dev_jm, dev_af...

-PASOS A SEGUIR PARA TRABAJAR:
Cambiamos a la rama dev y hacemos:  
git pull dev
Cambiamos a nuestra rama: 
git checkout dev_TU
Git rebase dev ¡¡¡ESTANDO EN NUESTRA RAMA, IMPORTANTE!!!

-Trabajamos lo que nos toque...

-Una vez queramos subir los cambios tenemos que hacer lo siguiente
Para pillar los cambios que han podido hacer el resto mientras estabas trabajando:
git pull dev
Y seguramente tendremos que resolver los conflictos que surjan:
git merge dev_TU
