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
