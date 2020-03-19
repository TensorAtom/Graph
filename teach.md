---
title: Label template
export_on_save:
    pandoc: false
output:
    word_document
---

Explain the basic introduction of labels and some superparameter settings of the labeling tool. The properties of the same group_id are independent of each other.

Set superparameters with Python syntax:

```python
kinds = "Motor vehicles", "Non-motor vehicles", "Pedestrian"
```

## Motor vehicles

Property|group_id|Is it a multi-choice|List of property values
:-|:-|:-|:-
car|0|0|2bmini,2bcar,3bcar,suv,Lsuv,MPV,Scar
truck|0|0|Ptruck,Mbus,Etruck,Ltruck
direction|1|0|front,left,right,rear,Rlateral,Llateral,Clateral
condition|2|0|whole,other

## Non-motor vehicles

Property|group_id|Is it a multi-choice|List of property values
:-|:-|:-|:-
type|0|0|bike,hood,tri,manpulled,cart
direction|1|0|front,left,right,rear,Rlateral,Llateral,Clateral
condition|2|0|whole,other
posture|3|0|upright,lean

## Pedestrian

Property|group_id|Is it a multi-choice|List of property values
:-|:-|:-|:-
ped1|0|1|man,byc,cart,umb,long,bag,carry,child
ped2|1|1|wheel,upbody,down,chair,old,crowd
direction|2|0|front,left,right,rear,Rlateral,Llateral,Clateral
condition|3|0|whole,other
