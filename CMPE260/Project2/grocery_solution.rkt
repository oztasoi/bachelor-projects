#lang scheme
; 2016400198

(define FARMS '(
(farmA 100 (apricot apple blueberry))
(farmB 90 (broccoli carrot grape))
(farmC 75 (corn grape lemon))
(farmD 75 ())
(farmE 45 (lemon melon olive berry))
(farmF 70 (lemon carrot))
(farmG 50 (olive))
(farmH 150 (olive grape apple))
(farmI 50 (apple))
(farmJ 45 (ginger beans garlic))
(farmK 70 (spinach onion peas))
(farmL 50 ())
(farmM 150 (spinach melon potato tomato))
(farmN 50 (spinach corn))
(farmO 50 (spinach))
))

(define CUSTOMERS '(
(john (farmA farmC) (apricot lemon))
(james (farmB farmC) (grape corn))
(arya (farmB farmD) (grape broccoli))
(elenor () ())
(alan (farmG farmH) (olive apple))
(george (farmF farmE farmG) (lemon melon olive apple))
(cersei (farmE farmF farmH farmI) (lemon olive apple))
(jon (farmA farmB farmC farmD farmE farmF farmG farmH farmI) (apricot apple blueberry broccoli
carrot grape corn lemon melon olive berry))
(sophia (farmK farmN farmO) (spinach onion corn))
(liam (farmM farmN farmO) (spinach melon potato))
(emma (farmD farmH farmK farmA) (apricot grape spinach))
(river (farmG farmB farmI farmA) (apple broccoli olive))
(lucas (farmK farmJ farmA farmD farmM farmN) (spinach onion apple))
(oliver (farmE farmF farmG) (lemon olive))
(zoe () ())
))

(define CROPS '(
(apricot farmA 10)
(apple farmA 12)
(melon farmE 22)
(olive farmE 40)
(berry farmE 10)
(lemon farmF 35)
(carrot farmF 5)
(olive farmG 60)
(olive farmH 30)
(blueberry farmA 15)
(broccoli farmB 8)
(carrot farmB 5)
(grape farmB 10)
(corn farmC 9)
(grape farmC 12)
(lemon farmC 10)
(lemon farmE 12)
(grape farmH 10)
(apple farmH 8)
(apple farmI 8)
(ginger farmJ 10)
(beans farmJ 13)
(garlic farmJ 15)
(spinach farmK 5)
(onion farmK 9)
(peas farmK 8)
(spinach farmM 10)
(melon farmM 15)
(potato farmM 9)
(tomato farmM 9)
(spinach farmN 7)
(corn farmN 9)
(spinach farmO 6)
))


(define (rcost farm cfarm)
  (if (eqv? cfarm '())
      0
      (if (eqv? (car (car cfarm)) farm)
          (car (cdr (car cfarm)))
          (rcost farm (cdr cfarm)))))

(define (ravailable farm cfarm)
  (if (eqv? cfarm '())
      '()
      (if (eqv? (car (car cfarm)) farm)
          (cdr (cdr (car cfarm)))
          (ravailable farm (cdr cfarm)))))

(define (rinterested name affiliation)
  (if (eqv? affiliation '())
      '()
      (if (eqv? (car (car affiliation)) name)
          (cdr (cdr (car affiliation)))
          (rinterested name (cdr affiliation)))))

(define (rcontract name affiliation)
  (if (eqv? affiliation '())
      '()
      (if (eqv? (car (car affiliation)) name)
          (car (cdr (car affiliation)))
          (rcontract name (cdr affiliation)))))

(define (farmcontract clist farm affiliation)
  (if (eqv? affiliation '())
      clist
      (if (member farm (car (cdr (car affiliation))))
          (farmcontract (append clist (list (car (car affiliation)))) farm (cdr affiliation))
          (farmcontract clist farm (cdr affiliation)))))

(define (interested clist crop affiliation)
  (if (eqv? affiliation '())
      clist
      (if (member crop (car (cdr (cdr (car affiliation)))))
          (interested (append clist (list (car (car affiliation)))) crop (cdr affiliation))
          (interested clist crop (cdr affiliation)))))

(define (minimum a b)
  (if (< a b)
      a
      b))

(define (minimum-price min crop cropslist)
  (if (eqv? cropslist '())
      (if (eqv? min '+inf.0)
          0
          min)
      (if (eqv? crop (car (car cropslist)))
              (minimum-price (minimum min (car (cdr (cdr (car cropslist))))) crop (cdr cropslist))
              (minimum-price min crop (cdr cropslist)))))

(define (boundary lower upper clist cropslist)
  (if (eqv? cropslist '())
      clist
      (if (and (< (car (cdr (cdr (car cropslist)))) (+ upper 1)) (> (car (cdr (cdr (car cropslist)))) (- lower 1)))
          (if (member (car (car cropslist)) clist)
              (boundary lower upper clist (cdr cropslist))
              (boundary lower upper (append clist (list (car (car cropslist)))) (cdr cropslist)))
          (boundary lower upper clist (cdr cropslist)))))

(define (help-me crop croplist crop-farm-list)
  (if (eqv? croplist '())
      crop-farm-list
      (if (eqv? crop (car (car croplist)))
          (help-me crop (cdr croplist) (append crop-farm-list (list(car (cdr (car croplist))))))
          (help-me crop (cdr croplist) crop-farm-list))))

(define (help-me-2 farmlist name finalfarmlist)
  (if (eqv? farmlist '())
      finalfarmlist
      (if (member (car farmlist) (CONTRACT-FARMS name))
          (help-me-2 (cdr farmlist) name (append finalfarmlist (list (car farmlist))))
          (help-me-2 (cdr farmlist) name finalfarmlist))))

(define (crop-in-farm farm crop croplist fee)
  (if (eqv? croplist '())
      fee
      (if (eqv? crop (car (car croplist)))
          (if (eqv? farm (car (cdr (car croplist))))
              (crop-in-farm farm crop (cdr croplist) (+ fee (+ (TRANSPORTATION-COST farm) (car (cdr (cdr (car croplist)))))))
              (crop-in-farm farm crop (cdr croplist) fee))
          (crop-in-farm farm crop (cdr croplist) fee))))

(define (listmaker crop farmlist feelist)
  (if (eqv? farmlist '())
      feelist
      (listmaker crop (cdr farmlist) (append feelist (list (crop-in-farm (car farmlist) crop CROPS 0))))))

(define (minmaker list min)
  (if (eqv? list '())
      min
      (minmaker (cdr list) (minimum min (car list)))))

(define (crop-bringer name croplist finalcroplist)
  (if (eqv? croplist '())
      finalcroplist
      (if (eqv? name (car (car croplist)))
          (crop-bringer name (cdr croplist) (append finalcroplist (car (cdr (cdr (car croplist))))))
          (crop-bringer name (cdr croplist) finalcroplist))))

(define (unite crops name totalfee)
  (if (eqv? crops '())
      totalfee
      (unite (cdr crops) name (+ totalfee (BUY-PRICE name (car crops))))))

(define (TRANSPORTATION-COST farm) (rcost farm FARMS))

(define (AVAILABLE-CROPS farm) (ravailable farm FARMS))

(define (INTERESTED-CROPS name) (rinterested name CUSTOMERS))

(define (CONTRACT-FARMS name) (rcontract name CUSTOMERS))

(define (CONTRACT-WITH-FARMS farm) (farmcontract '() farm CUSTOMERS))

(define (INTERESTED-IN-CROP crop) (interested '() crop CUSTOMERS))

(define (MIN-SALE-PRICE crop) (minimum-price '+inf.0 crop CROPS))

(define (CROPS-BETWEEN lower upper) (boundary lower upper '() CROPS))

(define (BUY-PRICE name crop) (minmaker (listmaker crop (help-me-2 (help-me crop CROPS '()) name '()) '()) '+inf.0))

(define (TOTAL-PRICE name) (unite (crop-bringer name CUSTOMERS '()) name 0))