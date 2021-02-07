(ns messy.events
  (:require
   [re-frame.core :as re-frame]
   [messy.db :as db]
   ))

(re-frame/reg-event-db
 ::initialize-db
 (fn [_ _]
   db/default-db))
