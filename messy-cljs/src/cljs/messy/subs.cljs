(ns messy.subs
  (:require
   [re-frame.core :as re-frame]))

(re-frame/reg-sub
 ::username
 (fn [db]
   (:username db)))

(re-frame/reg-sub
 ::messages
 (fn [db]
   (:messages db)))

(re-frame/reg-sub
 ::recipient
 (fn [db]
   (:recipient db)))

(re-frame/reg-sub
 ::content
 (fn [db]
   (:content db)))

(re-frame/reg-sub
 ::range
 (fn [db]
   (:range db)))
